package shareinfo;

import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

import javax.servlet.ServletConfig;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import com.google.gson.Gson;

import helper.db.*;
import helper.info.*;

public class MsgAjaxServlet extends HttpServlet {
	private static final long serialVersionUID = 1L;
	private MySQLdb mySQLdb;

	public void init(ServletConfig config) {
		System.out.println("---> Entering init() MsgAjax");
		mySQLdb = new MySQLdb();
		System.out.println("---> Exiting init() MsgAjax");
	}

	public void doGet(HttpServletRequest request, HttpServletResponse response)
			throws IOException, ServletException {
		
		System.out.println("---> Entering doGet() MsgAjax");

		ArrayList<MessageInfo> messageList = mySQLdb.getAllMessages();

		Gson gson = new Gson();
		String json = gson.toJson(messageList);
		System.out.println(json);

		response.setContentType("application/json");
		PrintWriter out = response.getWriter();
		out.println(json);
		out.flush();
		out.close();

		System.out.println(json);
		System.out.println("---> Exiting doGet() MsgAjax");
		
	}
}