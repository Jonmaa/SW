<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html>
<%@ page import="java.util.*,helper.info.*"%>
<%
ArrayList<MessageInfo> messageList = (ArrayList) request.getAttribute("messageList");
%>
<html>
<head>
<title>Lista de Mensajes</title>
</head>
<body>
	<header>
		<h3>Lista de Mensasjes</h3>
	</header>
	<table>
		<tr>
			<th>Usuario</th>
			<th>Mensaje</th>
		</tr>
		<%
		for (MessageInfo messageInfo : messageList) {
		%>
		<tr>
			<td><%=messageInfo.getUsername()%></td>
			<td><%=messageInfo.getMessage()%></td>
		</tr>
		<%
		}
		%>
	</table>
</body>
</html>