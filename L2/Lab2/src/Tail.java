import java.util.Scanner;

public class Tail {
    static public int n;
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
        tLines = new String[n]; //cyclic array
        Scanner sc = new Scanner(System.in);
        int index = 0;
        int size = 0;
        while (sc.hasNextLine()) {
            tLines[index] = sc.nextLine();
            size++;
            index = index == n - 1 ? 0 : index + 1;
        }

        if (n > size) {
            TooManyLines = true;
            prompt = "Zabraklo " + (n - size) + " linii do wypisania";
        }

        index = n > size ? 0 : size % n; // przejscie na początek linii do wypisywania
        n = Math.min(n, size);
        int i = 0;
        while (i < n) {
            System.out.println(tLines[index]);
            index = index == n - 1 ? 0 : index + 1;
            i++;
        }
        if (TooManyLines){
            if (!paramE) System.out.println(prompt);
            System.exit(2);
        }
        System.exit(0);
    }
}
