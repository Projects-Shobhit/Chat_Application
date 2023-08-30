# Chat_Application
Intranet Chat application using python socket library and tkinter tool.

The following is a proposal for a Chat Application project consisting of an intranet-based network used for the medium of communication. Our goal is to allow the user to send/receive text messages and communicate with multiple other users at the same time, making the application completely dynamic. 

The project involves both hardware and software requirements. In the hardware part we need a device to establish the server on, and other multiple devices with a keyboard and a mouse to operate. In the software part we will develop a server application and a client application using the Python3. The technology we will be using is the socket programming, multithreading and Tkinter library tool to develop the graphical user interface (GUI) for the chat application. The introduction and summary of these libraries is provided the main chapters attached in this report.

The application will be developed in three stages. In the first stage we will be developing the server application, that will use the IPv4 address of the system it is installed on. A client-side python code will be implemented to just connect the user to the server.

In the second stage, the main implementation will be done using the multithreading concept to facilitate the text-based chat feature between server and other clients. The application is based on a centralized server based network. 

Testing will be done in this stage using the Command Line Client (command prompt) in continuous stages. CMD will be used to test the first stage to establish communication, in the second stage to test the messaging/chat feature of the application.

Later, in the third stage Tkinter library will be used to develop the GUI of the chat application.

In such a manner, the whole project will be implemented in three stages. This project could lead to future projects involving more extensive inclusion of clients and server within the same network. This project will also be an excellent platform for the organizations to use within the premises to prevent security threats and information misuse.

# UPDATES:

Added the feature to send personal message to a single client in a connected environment.

Added a security feature with password-based user authentication.

Added the functionality of getting the current IP Address of the server system with the help of OS.
To correspond the changes, the dynamic binding of HOST and PORT in the client.py application file will be done after getting user-inputs of Server IP Address and PORT number. { YES, the user who is using the application will have to know the password, SERVER IP and PORT number and needs to enter them manually as a feature of security.}

![image](https://github.com/Projects-Shobhit/Chat_Application/assets/75949429/b13728bc-2a49-49b0-abaa-61973cdcb60e)

