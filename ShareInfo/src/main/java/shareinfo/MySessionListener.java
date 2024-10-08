package shareinfo;

import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import javax.xml.ws.spi.http.HttpContext;
 
public class MySessionListener implements HttpSessionListener {
 
	public void sessionCreated(HttpSessionEvent event) {
		System.out.println("---> Entrando en  sessionCreated() de MySessionListener" );
		System.out.println("     Una sesion esta siendo creada" );
		HttpSession session = event.getSession();
		System.out.println("     Session ID: " + session.getId());
		System.out.println("<--- Saliendo en  sessionCreated() de MySessionListener" );
			
	}
 
	public void sessionDestroyed(HttpSessionEvent event) {
		System.out.println("     --->Una sesion esta siendo destruida");
		HttpSession session = event.getSession();
				
		
		String sessionID = session.getId();
		System.out.println("     Cogiendo sessionID del usuario: " + sessionID);
		ServletContext context = session.getServletContext();
		HashMap<String, String> loggedinUsers = (HashMap) context.getAttribute("loggedin_users");
		System.out.println("     Loggedin users: " + loggedinUsers.toString());
		
		for(Map.Entry<String, String> entry : loggedinUsers.entrySet()) {
            if(entry.getValue().equals(sessionID)) {
            	loggedinUsers.remove(entry.getKey());
            	System.out.println("     Eliminando " + entry.getKey() + " de loggedin_users");
            	context.setAttribute("loggedin_users", loggedinUsers);
            	System.out.println("     Loggedin users: " + loggedinUsers.toString());
            	break;
            }
		}
		

		
	}
 
}

 