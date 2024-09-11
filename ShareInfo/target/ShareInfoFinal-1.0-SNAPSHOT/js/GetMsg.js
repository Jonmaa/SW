function GetMsg() {
	var request = new XMLHttpRequest();
	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			if (request.status == 200) {
				if (request.responseText != null) {
					var jsonObj = JSON.parse(request.responseText);
					var table = "<tr><th>Username</th> <th>Message</th></tr>";
					for (i = 0; i < jsonObj.length; i++) {
						table += "<tr><td>" + jsonObj[i].username + "</td>";
						table += "<td>" + jsonObj[i].message + "</td></tr>";
					}
					document.getElementsByClassName("msgtable")[0].innerHTML = table;
				}
			}
		}
	};
	request.open("GET", "/ShareInfo/servlet/MsgAjaxServlet", true);
	request.send(null);
	setTimeout("GetMsg()", 1000);
}
