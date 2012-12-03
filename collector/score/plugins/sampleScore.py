import utils.settings as Settings
from collector.base import PluginBase
from subprocess import call

import subprocess

datadigestDir = str(Settings.SETTINGS.get("score","datadigestDir"))

pyPath = "-Dpython.path=" + str(datadigestDir)
jythonExe = "./score/JythonBI.py"

data_file = "./score/models/out_sample.csv"
model_file = "./score/models/Skaion_model.bn5"
outs = ["OUTCOME", "Two"]
thrus = ["OUTCOME"]

# call(["jython", pyPath, jythonExe, data_file, model_file, str(outs), str(thrus)])
results = subprocess.Popen(["jython", pyPath, jythonExe, data_file, model_file, str(outs), str(thrus)], \
                 stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]

s = subprocess.Popen(['cowsay', 'hello'], \
      stderr=subprocess.STDOUT, stdout=subprocess.PIPE).communicate()[0]
      
print s
print results