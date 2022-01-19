from socket import *
import base64
import time


endmsg = "\r\n.\r\n" #printing end message '.' which exits the mail command and send it.

# Choose a mail server (e.g. Google mail server) and call it mailserver
mailserver = ("dtu-dk.mail.protection.outlook.com",25) #DTU SERVER: "dtu-dk.mail.protection.outlook.com"

# Create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect(mailserver) #Writing the mailserver into the terminal.
recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != '220':
    print('220 reply not received from server.')


# Send HELO command and print server response. Using EHLO for Extended Simple Mail Transfer Protocol (ESMTP). This is because im using the MIME format.
heloCommand = 'EHLO Alice\r\n' # EHLO for extended SMTP
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != '250':
 print('250 reply not received from server.')

# Send MAIL FROM command and print server response.
mailFrom = "MAIL FROM: <"
mail = input("Mail from: ")
end = ">\r\n"
clientSocket.send(mailFrom.encode() + mail.encode() + end.encode()) #writing the MAIL FROM command in terminal
recv2 = clientSocket.recv(1024)
recv2 = recv2.decode()
print("After MAIL FROM command: " +recv2) #printing response

# Send RCPT TO command and print server response.
rcptTo = "RCPT TO: <"
mailTo = input("Mail to: ")
clientSocket.send(rcptTo.encode() + mailTo.encode() + end.encode()) #writing the RCPT TO: command in the terminal
recv3 = clientSocket.recv(1024)
recv3 = recv3.decode()
print("after RCPT TO command: "+recv3)


# Send DATA command  and print server response.
data = "DATA\r\n"
clientSocket.send(data.encode()) #Writing the DATA command in the terminal
recv4 = clientSocket.recv(1024)
recv4 = recv4.decode()
print("After DATA command "+recv4)



# Send message data.
subject = "Subject: "
subjectInput = input("Write your subject: ") #creating a subject for the mail.
clientSocket.send(subject.encode() + subjectInput.encode()) #writing the subject into the terminal.
clientSocket.send("\r\n".encode())
clientSocket.send("MIME-Version: 1.0\r\n".encode()) #including MIME extension (To include pictures.)
clientSocket.send("Content-Type: multipart/mixed; boundary=X\r\n\r\n".encode()) #setting content type to multipart/mixed for enabling more than 1 format. (text/image). Boundary set to X

clientSocket.send("This is a MIME formatted text MSG. If you see this it's you can't view the original mail.\r\n".encode()) #If the user sees this text, the users mail client doesn't support MIME formatted emails.

clientSocket.send("--X\r\n".encode()) #inserting boundary
clientSocket.send("Content-Type: text/plain\r\n\r\n".encode()) #defining current content-type within boundary.
msg = input("Write the body of your mail here: \n") #creating body of the email
clientSocket.send(msg.encode()) #Sending the msg to the terminal
clientSocket.send("\r\n".encode())

clientSocket.send("--X\r\n".encode()) #inserting boundary
clientSocket.send("Content-Type: image/jpg\r\n".encode()) #defining content type
clientSocket.send("Content-Disposition:attachment;filename=image.jpg\r\n".encode()) #Creating name for attachment.
clientSocket.send("Content-Transfer-Encoding:base64\r\n\r\n".encode()) #use base64 encoding for the image.
path = input("Write the path of your image. If image is in same path, write only the name:\n") #User input for image.
with open(path, "rb") as image_bit: #open the image in the requested path.
    converted_string = base64.b64encode(image_bit.read()) #convert the image to string type
clientSocket.send("\r\n".encode())
clientSocket.send(converted_string) #send the converted image to the terminal.
clientSocket.send("\r\n".encode())
clientSocket.send("--X--".encode()) #end boundary here. (notice ending '--')

clientSocket.send(endmsg.encode()) #endmsg command send here. '.'
recv_msg = clientSocket.recv(1024)
print("Response after sending message body:"+recv_msg.decode())
quit = "QUIT\r\n"
clientSocket.send(quit.encode()) #write the QUIT command in the terminal
recv5 = clientSocket.recv(1024)
print(recv5.decode())
clientSocket.close() #close the clientSocket.
# Fill in end
