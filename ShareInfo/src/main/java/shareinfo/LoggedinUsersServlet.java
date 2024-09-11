package shareinfo;

import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;


public class LoggedinUsersServlet extends HttpServlet{

	private static final long serialVersionUID = 1L;
	
	 
    public void doGet(HttpServletRequest request, HttpServletResponse response)
        throws ServletException, IOException {
    	System.out.println("---> doGet() de loggedinUsersServlet");
    	
    	HttpSession session = request.getSession();
    	System.out.println(session.getId());
    	ServletContext context = session.getServletContext();
    	System.out.println(context.getContextPath());
    	
    	String salida="";
    	
    	response.setContentType("text/plain");
		HashMap<String, String> loggedinUsers = (HashMap<String, String>) context.getAttribute("loggedin_users");
		
		//System.out.println("     Loggedin users: " + context.getAttribute("loggedin_users").toString());
		for (Map.Entry<String, String> entry : loggedinUsers.entrySet()) {
				salida= salida + entry.getKey() + ";";
		}
	   
			
	    PrintWriter out = response.getWriter();
		out.println(salida);
	    out.flush();
		out.close();

		System.out.println("<--- DoGet() en loggedinUsersServlet");
}
}

