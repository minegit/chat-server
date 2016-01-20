# chat-server
A simple REST API based chat server.

#Project setup

This project requires
	1. Django (Installed)
	2. mysql (installed with proper cred)
	3. python libraries

Please update my,cnf according to your mysql creds.

Then run python manage.py run migrations
Then run the app by python manage.py runserver 8000

It will run the server in the localhost:8000/ port.


REST API :
	1. An api send message from a user  to another user.
		http://127.0.0.1:8000/chat/send?from=2&to=3&msg=asdsd23

		Response : 
			{
				status: 200,
				message: "Suitable Message"       // status will be 200 in case of successfull response.
			}

			or 

			{
				status: 201,
				message: "Suitable Message"        // in case of any error status will not be 200
			}
	2.An api to get all the new messages for a user send from another user.
		http://127.0.0.1:8000/chat/get?user_id=31&from_id=2
		from_id is optional here. If it is given then it pick new messages
		from this user only otherwise all the messages from all the users will be fetched.

		{
			status: 200,
			message: [
				"asdsd23"
				]
			}

		or
		{
				status: 201,
				message: "Suitable Message"        // in case of any error status will not be 200
			}
