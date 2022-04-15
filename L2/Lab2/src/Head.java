import java.util.Scanner;

public class Head {

    static public int n = 0;
    static public Boolean paramE = false;
    static String[] tLines;
    static public Boolean TooManyLines = false;
    static public String prompt = "";

    public static void main(String[] args) {

        for (String arg : args) {
            if (arg.contains("--lines="))
                n = Integer.parseInt(arg.substring(arg.indexOf("=") + 1));
            if (arg.equals("-e"))
                paramE = true;
        }

        Scanner sc = new Scanner(System.in);
        tLines = new String[n];
        int index = 0;
        while (sc.hasNextLine()) {
            if (index < n) {
                tLines[index] = sc.nextLine();
            } else {
                sc.nextLine();
            }
            index++;
        }
        if (n > index) {
            TooManyLines = true;
            prompt = "Zabraklo " + (n - index) + " linii do wypisania";
        }

        n = Math.min(n, index);
        for (int i = 0; i < n; i++) {
            System.out.println(tLines[i]);
        }

        if (TooManyLines) {
            if (!paramE) System.out.println(prompt);
            System.exit(2);
        }
        System.exit(0);
    }
}
