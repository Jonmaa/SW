package shareinfo;

import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;

import com.google.gson.Gson;

 
public class TimeAjaxServlet extends HttpServlet {

	public void doGet(HttpServletRequest request, HttpServletResponse response)
               throws IOException, ServletException {
		Calendar cal = Calendar.getInstance();
    	response.setContentType("text/xml");
		PrintWriter out = response.getWriter();
		
		out.print("<?xml version=\"1.0\"?>");
		out.print("<time>");
        out.print("<hour>" + cal.get(Calendar.HOUR_OF_DAY) + "</hour>");
        out.print("<minute>" + cal.get(Calendar.MINUTE) + "</minute>");
        out.print("<second>" + cal.get(Calendar.SECOND) + "</second>");
        out.print("</time>");
        
        out.flush();
        out.close();
        
    	// Log
    	System.out.println("XML ntp servlet has been hit"); 
    	System.out.println(cal.getTime());  
   }
   
	public void doPost(HttpServletRequest request, HttpServletResponse response)
               throws IOException, ServletException {     	
		Calendar cal = Calendar.getInstance();
    	response.setContentType("application/json");
		PrintWriter out = response.getWriter();
		
		HashMap<String, Object> hashMap = new HashMap<String, Object>();
		hashMap.put("hour",cal.get(Calendar.HOUR_OF_DAY));
		hashMap.put("minute",cal.get(Calendar.MINUTE));
		hashMap.put("second",cal.get(Calendar.SECOND));
		
		Gson gson = new Gson();
      	String json = gson.toJson(hashMap);
      	response.setContentType("application/json");
        
      	out.println(json);
        out.flush();
        out.close();
        
    	// Log
    	System.out.println("JSON ntp servlet has been hit"); 
    	System.out.println(json); 
   }
   
}