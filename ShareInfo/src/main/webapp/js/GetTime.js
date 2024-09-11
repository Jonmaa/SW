function GetTimeIO() {
	nocache = "nocache=" + Math.random() * 1000000;
	var request = new XMLHttpRequest();
	
	request.onreadystatechange = function() {
	if (request.readyState == 4) {
		if (request.status == 200) {
			if (request.responseXML != null) {
				
				hour = this.responseXML.getElementsByTagName("hour")[0].childNodes[0].nodeValue;
				document.getElementsByClassName("hour")[0].innerHTML = hour;
				minute = this.responseXML.getElementsByTagName("minute")[0].childNodes[0].nodeValue;
				document.getElementsByClassName("minute")[0].innerHTML = minute;
				second = this.responseXML.getElementsByTagName("second")[0].childNodes[0].nodeValue;
				document.getElementsByClassName("second")[0].innerHTML = second;
				data = new Date();
				hcliente= data.getHours() + ":" + data.getMinutes() + ":" + data.getSeconds();
				document.getElementsByClassName("hcliente")[0].innerHTML = hcliente;
				}
		}
	}
};

request.open("GET", "/ShareInfo/servlet/getTime?" + nocache, true);
request.send(null);
setTimeout("GetTimeIO()",5000);}
