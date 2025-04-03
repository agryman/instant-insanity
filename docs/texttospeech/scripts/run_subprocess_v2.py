import subprocess
import sys

def run_win_cmd(cmd):
    result = []
    process = subprocess.Popen(cmd,
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    for line in process.stdout:
        result.append(line)
    errcode = process.returncode
    for line in result:
        outputline = line
        outputline = line.decode('utf-8')
        outputline = outputline.rstrip()
        print(outputline)
    if errcode is not None:
        raise Exception('cmd %s failed, see above for details', cmd)
    
if len(sys.argv) > 1:
    argument = sys.argv[1]
    inputfile = argument
    #print(f"Argument: {argument}")
else:
    print("No argument provided.")
    sys.exit()

txtfilename=argument
programname = argument.split(".")[0]
vbsfilename = txtfilename.split(".")[0] + ".vbs"
audiofilename = txtfilename.split(".")[0] + ".wav"

print(" program name = %s" % (programname))
print(" txtfile name = %s" % (txtfilename))
print(" vbsfile name = %s" % (vbsfilename))
print(" audiofile name = %s\n" % (audiofilename))

speaklines = []

with open(inputfile, 'r') as file:
    for line in file:
        # Process each line
        speaklines.append(line.strip())
        print(line.strip())


vbsfilecontent = """
Const SAFT48kHz16BitStereo = 39 
Const SSFMCreateForWrite = 3
Dim oFileStream, oVoice 
Dim Voices(100) 
Set oFileStream = CreateObject("SAPI.SpFileStream") 
oFileStream.Format.Type = SAFT48kHz16BitStereo 
"""

vbsfilecontent += "oFileStream.Open " + "\"" + audiofilename + "\", SSFMCreateForWrite\n"

vbsfilecontent += """
Set oVoice = CreateObject(\"SAPI.SpVoice\") 
Set oVoice.AudioOutputStream = oFileStream 
Set sapi = createObject(\"sapi.spvoice\") 
WScript.Echo (\"number of voices \" & oVoice.GetVoices.Count) 
Set oVoice.Voice = oVoice.GetVoices.Item(1) 
WScript.Echo (\"voice volume \" & oVoice.Volume) 
WScript.Echo (\"voice rate \" & oVoice.Rate)  
WScript.Echo (\"voice selected \" & \"1\") 
"""

for line in speaklines:
    vbsfilecontent += "oVoice.Speak " + "\"" + line + "\"\n"
    
vbsfilecontent +=  "oFileStream.Close\n"

with open("temp.vbs","w") as f:
    f.writelines(vbsfilecontent)

cmd = "C:\\WINDOWS\\SysWoW64\\cscript " + "temp.vbs"

run_win_cmd(cmd)