function GetUsers() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function()
	{
		if (request.readyState == 4) 
		{
			if (request.status == 200) 
				
			{
				if (request.responseText != null) 
				{
					console.log( request.responseText)
					var section = " Usuarios Activos:" + request.responseText;
					document.getElementsByClassName("ActiveUsers")[0].innerHTML = section;
				}
			}
		};
	};
		
	request.open("GET", "/ShareInfo/servlet/LoggedinUsersServlet", true);
	request.send(null);
	setTimeout("GetUsers()", 1000);
	}
