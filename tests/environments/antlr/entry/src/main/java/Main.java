import hello.LangLexer;
import hello.LangParser;

import java.io.IOException;
import java.io.PrintWriter;
import java.io.FileWriter;

class Main {
  public static void main(String [] args) {
    String file_name = args[0];

    if (file_name.equals("exit")) {
      System.out.println("exiting");
      System.exit(1);
    }

    try (PrintWriter print_writer = new PrintWriter(new FileWriter(file_name))) {
      print_writer.printf("%s\n", "hello");
    } catch (IOException exception) {
      System.exit(1);
    }

    System.exit(0);
  }
}
