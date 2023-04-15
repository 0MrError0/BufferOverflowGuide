# BufferOverflowGuide


## Hii..! Hackers Welcome 

### Brainpan is a vulnerable virtual machine designed for New students who are intrested to learn bufferoverflow or who are going to answer the oscp Examination. So in this github Page i will going show you how to exploit brainpan.exe. Well i will not going to start from the begnning like scanning the brainpan machine as i have already scaned the Machine and found Brainpan.exe in /bin path at port 10000 which was of python http server 



>***Requiments :- Immunity Debugger , VirtualBox in Windows7.***



### As i was facing some issue with my windows7 machine i use my host machine to exploit this brainpan.exe file 



>***Aim :- Exploiting BrainPan.exe and gaining Reverse Shell Access***



***NOTE :- Make sure that You Trun Off Your Anitvirus and Windows defender*** 

### Open Immunity Debugger in Administrator Mode and click on file >> open >> and select the brainpan.exe file! then click on the paly button so that the brainpan.exe is in running mode



![base1](https://user-images.githubusercontent.com/102399357/232192974-d27a2cdc-ba1c-469e-9147-792f0c30cdad.PNG)

### Then the .exe will start Running on the Host With Port Number 9999

![runnning](https://user-images.githubusercontent.com/102399357/232191959-ab9db141-5b4f-4e98-a922-214048c3bbd5.PNG)


### As we Now know that the .exe is serving on port 9999 now let us Fuzz the input of the brainpan.exe 

***What is Fuzzing ? <br />
In programming and software development, fuzzing or fuzz testing is an automated software testing technique that involves providing invalid, unexpected, or random data as inputs to a computer program. The program is then monitored for exceptions such as crashes, failing built-in code assertions, or potential memory leaks. Typically, fuzzers are used to test programs that take structured inputs <br /> (Shameless copied from Wikipedia)*** 



## Step 1 Fuzzing <br />
### The Following Python Script is Used to Fuzz The brainpan.exe service <br />

```python
import socket
import sys
import time

IP="192.168.94.131"

i=100
while True:
	try:
		with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
			c.settimeout(5)
			c.connect((IP,9999))
			c.recv(9999999)
			string="A"*i
			c.send(bytes(string+" \r\n",'utf-8'))
			print("[+]"+str(i)+" Bytes Sent..!")
			time.sleep(1)
			c.recv(9999999)

	except:
		print("[!]Crashed at "+str(i)+" Bytes")
		sys.exit(0)
	i=i+100
```
***In The First Line of Code i have Imported some modules. I have declared some variables IP ( To set Ip Addr ) and i value to 100 for Counter purpose. Now in while True loop which is infinet loop i have added try and except block in which i have created a socket object refeared as c in which i set the timeout to 5 sec and then connect to the desire Ip address and Port Number of my Host machine. following that we recive the bufffer which is the banner and Enter Password Text after receving the buffer i have created the string variable in which i create "A" into 100 times at the first entry time and then we send the string with "\r\n" which is Used as a new line character in Windows And then we print how may bytes was send of "A" 's and then we recv the buffer saying that Access Denied in except block we print out that at how many bytes the program was crashed and then exit the program and if the the program was not crashed it incriments the i value t0 +100. and the program is continued until the .exe is being crashed...!***<br />


>***Python3 Fuzz.py***
<br />

![Fuzz](https://user-images.githubusercontent.com/102399357/232196177-caed504b-2f25-4b97-bda8-55a3b546e20b.PNG)

### As Soon as we run the script we see that the .exe Program gets Crashed at  600 bytes As We can see that the all the registors and EIP is Also gets overwritten with 41 which is "A" in hex format  <br />

![immuFuzz](https://user-images.githubusercontent.com/102399357/232196264-1670e72a-9ea2-4fdb-97ef-0f0dfb3109e3.PNG)

### Now we know that our .exe was crashing at 600 bytes but we actually dont know the Exact offset value 

***what is offset? <br />
   When you are overflowing a buffer to write on the stack in a way which is exploitable you will overwrite the return address on the stack. Ie, sending a long string of AAAAAAAAAAAAAAAAAAAAAAAAAAA.....AAAAAAAAA will result in EIP containing the value 0x41414141 when the application crashes.***

**Now assume that if we pass "A" into 10 times + "B" into 4 times and in EIP we see that the EIP value is 42424242 so the offset will be 10bytes Because we see that after 10 "A"'s any value we provide to the string it gets overwritten to the EIP value**


