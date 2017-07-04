import os, winshell


startup = winshell.startup()

if "TestCam.lnk" in os.listdir(startup):
    print("True")
else:
    target = os.path.join(winshell.desktop(),'TestCamBot.pyw')
    winshell.move_file(target, winshell.programs())
    target= os.path.join(winshell.programs(),'TestCamBot.pyw')
    path = os.path.join(startup,'TestCamBot.lnk')
    winshell.CreateShortcut(path, target,
                           "TOKEN [optional id of user to send privately]")
                           
