## File Transfer Protocol ##
### A P2P protocol for inter-system communication written ini python ###
#### Instructions ####
- "FileUpload [filename]" to send the file the server side.
- "FileDownload [filename]" to download the file from the server side.
- "ls" to list all files in this directory of the client side.
- "lls" to list all files in the server side.
- "IndexGet shortlist <starttimestamp> <endtimestamp>" to list the files modified in mentioned timestamp.
- "IndexGet longlist" similar to shortlist but with complete file listing.
- "FileHash verify <filename>" checksum of the modification of the mentioned file.  
- "quit" to exit.

-----------------------------------------------------
### How to run ###
To run client use command ```python client.py```, and to run server use command ```python server.py```.  
#### Inter-system communication ####
Keep the `HOST='0.0.0.0' `in server.py unmodified.  
Make the `HOST='IP'` where `IP='IP address of the host'` inside the ```client.py```.  
#### Intra-system communication ####
make `HOST='localhost'` in both `server.py` and `client.py`,

-----------------------------------------------------
