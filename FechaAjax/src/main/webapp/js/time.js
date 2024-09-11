function GetTimeIO() {
	nocache = "nocache=" + Math.random() * 1000000;
	var request = new XMLHttpRequest();

	request.onreadystatechange = function() {
		if (request.readyState == 4) {
			if (request.status == 200) {
				if (request.responseXML != null) {
					day = this.responseXML.getElementsByTagName("day")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("day")[0].innerHTML = day;
					month = this.responseXML.getElementsByTagName("month")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("month")[0].innerHTML = month;
					year = this.responseXML.getElementsByTagName("year")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("year")[0].innerHTML = year;
					hour = this.responseXML.getElementsByTagName("hour")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("hour")[0].innerHTML = hour;
					document.getElementsByClassName("hour2")[0].innerHTML = hour;
					minute = this.responseXML.getElementsByTagName("minute")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("minute")[0].innerHTML = minute;
					document.getElementsByClassName("minute2")[0].innerHTML = minute;
					second = this.responseXML.getElementsByTagName("second")[0].childNodes[0].nodeValue;
					document.getElementsByClassName("second")[0].innerHTML = second;
					document.getElementsByClassName("second2")[0].innerHTML = second;

				}
			}
		}
	};

	request.open("GET", "/FechaAjax/servlet/getTime?" + nocache, true);
	request.send(null);
	setTimeout("GetTimeIO()", 5000);
}
