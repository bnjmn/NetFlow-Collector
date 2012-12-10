library( XML , quietly=TRUE)
#####################
args <- commandArgs(TRUE)

  if ( length(args) != 2 ) {
    # TODO: ADD some error code for bad args
    print("Input and output files not specified. Using defaults (may produce errors).")
    #	print("Use <Path>\Rscript.exe scoring_script3.R <sBI_file> <model_file>")
  } else {
    BIfile <- args[1]
    modelFile <- args[2]
    unconnectedVars <- args[3]
  }
  # This is specific to the "Geo 5b5 AS Query Using NoA Binning All Parts.bn5" model
  # TODO: Implement function to extract unconnected nodes
    unconnectedVars <- c("tcp_flag_URG")
    
  model <- xmlTreeParse( modelFile, useInternal = TRUE)

  ######## PARSE XML #######
  top <- xmlRoot(model)
  ##### get StateNames Here
  varInfo <- xmlSApply( top[["DEFAULT_MODEL"]][["BNMODEL"]][["VARIABLES"]],
                        function(x) xmlSApply(x, names))
  M <- dim(varInfo)[2]
  
  ##### info1: field, numLevels, cumLevel, factLevels
  info1 <- data.frame( row.names = 1:dim(varInfo)[2], stringsAsFactors = FALSE,
                       cbind( 
                         field = xmlSApply(top[["DEFAULT_MODEL"]][["BNMODEL"]][["VARIABLES"]], xmlAttrs),
                         numLevels = as.numeric(sapply(varInfo[3,], length)),
                         cumLevel = cumsum(as.numeric(sapply(varInfo[3,], length)))
                       )
  )
  factLevels <- NULL
  for (i in 1:(dim(varInfo)[2]) ) {
    factLevels <- rbind(factLevels, list(
      xmlSApply( top[["DEFAULT_MODEL"]][["BNMODEL"]][["VARIABLES"]][[i]][["STATENAMES"]], xmlAttrs)))
  }
  info1 <- cbind( info1, factLevels)
  info1 <- transform( info1, numLevels = as.numeric(numLevels), cumLevel = as.numeric(cumLevel))
  
  ########## info2: field, BinningMethod, DataType
  middle <- top[["DEFAULT_MODEL"]][["DISCRETIZATION"]][["VARIABLES"]]
  N <- length( xmlSApply( middle, xmlAttrs) )
  
  info2 <- data.frame(  row.names = 1:N, stringsAsFactors = FALSE,
                        cbind(
                          field = xmlSApply( middle, xmlAttrs),
                          BinningMethod = xmlSApply( middle, function(x) xmlGetAttr(x[["BINNINGMETHOD"]], "NAME")),
                          DataType = xmlSApply( middle, function(x) xmlGetAttr(x[["DATATYPE"]], "NAME"))
                        )
  )

  ##### Final INFO
  info <- merge( info2, info1, by = "field", all = TRUE)
  ##### Through vars
  Thrus<-subset(info,info$BinningMethod=="THROUGH")$field
  if(length(Thrus)>0){
    names(Thrus)<-"Thrus"
  }
  info<-subset(info,info$BinningMethod!="THROUGH")
  ##Return either Thrus and info or just info
  if(length(Thrus)>0){
    model_summary<-c(Thrus,info)
  }else{
    model_summary<-info
  }
  # print(model_summary)

#########################XML DATA Processed################################
#### Begin Scoring Algorithm ####
# M = number of fields in model, N = total fields in CSV
output_scoring<-function(BIfile,model_summary,unconnectedVars){
  ###Initiate vars
  M<-length(model_summary$field)
  Thru_data_frame<-data.frame()
  ##recreate Thrus and info
  if(length(model_summary$Thrus)>0){
    Thrus<-model_summary$Thrus
    info<-data.frame(cbind(model_summary$field,model_summary$BinningMethod,model_summary$DataType,model_summary$numLevels,model_summary$cumLevel,model_summary$factLevels))
    names(info)<-c("field","BinningMethod","DataType","numLevels","cumLevel","factLevels")
    info$numLevels<-as.numeric(as.vector(info$numLevels))
    info$cumLevel<-as.numeric(as.vector(info$cumLevel))
    #numThru <- length(model_summary$Thrus)
  }else{
    #numThru<-0
    info<-model_summary
  }
  
  ##initiate buffer
  buffer <- 1 + M  #################################################
  
  #Read in Batch Inference output
  BI <- read.csv( BIfile )
  ###Take out Through vars
  if(length(model_summary$Thrus)>0){
    Thru_data_frame<-subset(BI,select=Thrus)
    BI<-BI[,!(names(BI) %in% Thrus)]
  }
  
  TEMP <- NULL
  TEMP <- BI[,1]
  ###Take out unconnectedVars
  info <- subset(info,info$field!=unconnectedVars)
  M <- M - length(unconnectedVars)
  for (fieldRec in 1:M) {
    
    fieldInfo <- NULL #Store all Info applicable to current field here
    
    fieldName <- info[fieldRec,"field"]
    fCol <- buffer + (info[fieldRec,"cumLevel"] - info[fieldRec,"numLevels"] + 1)
    lCol <- buffer + info[fieldRec,"cumLevel"]
    fieldInfo <- cbind( PRIOR = BI[,which(names(BI)==fieldName)], BI[,fCol:lCol] ) 
    position <- apply( fieldInfo[,2:dim(fieldInfo)[2]], 1, which.max) 
    posterior <- apply( fieldInfo[,2:dim(fieldInfo)[2]], 1, max)
    prediction <- info[ fieldRec, "factLevels"][[1]][position]
    if(prediction[1]=="1.0"||prediction[1]=="0.0"){
      prediction<-substr(prediction,1,1)
    }
    flag <- ( fieldInfo[,1] == prediction )
    
    fieldInfo <- cbind( fieldInfo, position, posterior, prediction, flag )
    names(fieldInfo)[1] <- paste(fieldName,"_",names(fieldInfo)[1], sep="")
    names(fieldInfo)[(dim(fieldInfo)[2]-3):(dim(fieldInfo)[2])] <- c( 
      paste(fieldName,"_",toupper(names(fieldInfo)[(dim(fieldInfo)[2]-3)]), sep=""),
      paste(fieldName,"_",toupper(names(fieldInfo)[(dim(fieldInfo)[2]-2)]), sep=""),
      paste(fieldName,"_",toupper(names(fieldInfo)[(dim(fieldInfo)[2]-1)]), sep=""),
      paste(fieldName,"_",toupper(names(fieldInfo)[(dim(fieldInfo)[2])]), sep="")
    )
    TEMP <- cbind(TEMP, fieldInfo )
  }
  
  ###Score each record; ifElse to handle single record case
  if(dim(TEMP)[1] == 1) {
    TEMP <- cbind( TEMP, TOTAL_SCORE =   
                     sum(sapply(TEMP[,sapply(TEMP,class) == "logical"], as.numeric ))/(M) )
    
  } else {
    TEMP <- cbind( TEMP, TOTAL_SCORE =   
                     apply(sapply(TEMP[,sapply(TEMP,class) == "logical"], as.numeric ), 1, sum)/(M) )    
  }
  write(TEMP$TOTAL_SCORE, stdout())
}

## Call that^! function
output_scoring(BIfile, model_summary, unconnectedVars)
