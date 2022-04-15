import java.util.ArrayList;
import java.util.Scanner;

public class process {
    static public Boolean ignoreF = false, ignoreL = false, delimiter = false, project = false, select = false;
    static public int igFN = 0, igLN = 0;
    static public String delim_str = ",", sep = "\t\t", sel_str = "";
    static public String[] columns;

    public static void main(String[] args) {

        for (String arg : args) {
            if (arg.contains("--ignorefirst=")) {
                ignoreF = true;
                igFN = Integer.parseInt(arg.substring(arg.indexOf("=") + 1));
            }
            if (arg.contains("--ignorelast=")) {
                ignoreL = true;
                igLN = Integer.parseInt(arg.substring(arg.indexOf("=") + 1));
            }
            if (arg.contains("--delimiter=")) {
                delimiter = true;
                if(!arg.substring(arg.indexOf("=") + 1).equals("")){
                    delim_str = arg.substring(arg.indexOf("=") + 1);
                }
            }
            if (arg.contains("--separator=")) {
                delimiter = true;
                sep = arg.substring(arg.indexOf("=") + 1);
            }
            if (arg.contains("--project=")) {
                project = true;
                delimiter = true;
                columns = arg.substring(arg.indexOf("=") + 1).split(",");
            }
            if (arg.contains("--select=")) {
                select = true;
                sel_str = arg.substring(arg.indexOf("=") + 1);

            }
        }

        ArrayList<String> lines = read();

        if (lines.size() == 0) {
            System.exit(2);
        }

        ArrayList<String> returnLines = new ArrayList<>(lines.size());

        for (String line : lines) {
            if (line.length() != 0){
                if (ignoreF) line = line.substring(igFN);
                if (ignoreL) line = line.substring(0, line.length() - igLN);
                if (delimiter) line = line.replaceAll(delim_str, sep);
                if (project) {
                    String[] splittedLine = line.split(sep);
                    StringBuilder pro = new StringBuilder();
                    for (String c : columns) {
                        if (Integer.parseInt(c) <= splittedLine.length)
                            pro.append(splittedLine[Integer.parseInt(c) - 1]).append(sep);
                            //pro.append(String.format("%-22s",splittedLine[Integer.parseInt(c) - 1]));
                    }
                    line = pro.toString();
                }
                if (select && line.contains(sel_str)) {
                    returnLines.add(line);
                } else {
                    if (!select) returnLines.add(line);
                }
            }
        }

        if (returnLines.size() == 0) {
            System.exit(1);
        }

        for (String s : returnLines) {
            System.out.println(s);
        }

        System.exit(0);
    }


    private static ArrayList<String> read() {
        Scanner sc = new Scanner(System.in);
        ArrayList<String> lines = new ArrayList<>();

        while (sc.hasNextLine()) {
            lines.add(sc.nextLine());
        }
        return lines;
    }

}
