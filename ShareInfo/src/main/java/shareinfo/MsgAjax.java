package shareinfo;

import java.io.*;
import java.util.*;
import javax.servlet.*;
import javax.servlet.http.*;
import com.google.gson.Gson;
import helper.db.*;
import helper.info.*;

public class MsgAjax extends HttpServlet {
    private MySQLdb mySQLdb;

    public void init(ServletConfig config) {
        System.out.println("---> Entering init() MsgAjax");
        mySQLdb = new MySQLdb();
        System.out.println("---> Exiting init() MsgAjax");
    }
    public void doGet(HttpServletRequest request, HttpServletResponse response) throws
            IOException, ServletException {
        System.out.println("---> Entering doGet() MsgAjax");
        ArrayList<MessageInfo> messageList= mySQLdb.getAllMessages();
        Gson gson = new Gson();
        String json = gson.toJson(messageList);
        System.out.println(json);

        response.setContentType("application/json");
        PrintWriter out = response.getWriter();
        out.println(json);
        out.flush();
        out.close();

        System.out.println(json);
        System.out.println("---> Exiting doGet() MsgAjax");}}
