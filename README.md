# BufferOverflowGuide


## Hii..! Hackers Welcome 

### Brainpan is a vulnerable virtual machine designed for New students who are intrested to learn bufferoverflow or who are going to answer the oscp Examination. So in this github Page i will going show you how to exploit brainpan.exe. Well i will not going to start from the begnning like scanning the brainpan machine as i have already scaned the Machine and found Brainpan.exe in /bin path at port 10000 which was of python http server 



>***Requiments :- Immunity Debugger , VirtualBox in Windows7.***



### As i was facing some issue with my windows7 machine i use my host machine to exploit this brainpan.exe file 



>***Aim :- Exploiting BrainPan.exe and gaining Reverse Shell Access***



***NOTE :- Make sure that You Trun Off Your Anitvirus and Windows defender*** 

## Open Immunity Debugger in Administrator Mode and click on file >> open >> and select the brainpan.exe file! then click on the paly button so that the brainpan.exe is in running mode



![base1](https://user-images.githubusercontent.com/102399357/232192974-d27a2cdc-ba1c-469e-9147-792f0c30cdad.PNG)

### Then the .exe will start Running on the Host With Port Number 9999

![runnning](https://user-images.githubusercontent.com/102399357/232191959-ab9db141-5b4f-4e98-a922-214048c3bbd5.PNG)

<br />
### As we Now know that the .exe is serving on port 9999 now let us Fuzz the input of the brainpan.exe 
<br /><br />
***What is Fuzzing ? <br /><br />
In programming and software development, fuzzing or fuzz testing is an automated software testing technique that involves providing invalid, unexpected, or random data as inputs to a computer program. The program is then monitored for exceptions such as crashes, failing built-in code assertions, or potential memory leaks. Typically, fuzzers are used to test programs that take structured inputs <br /> (Shameless copied from Wikipedia)*** 

<br /><br />

## Step 1 Fuzzing <br />
### The Following Python Script is Useed to Fuzz The brainpan.exe service <br /><br />



