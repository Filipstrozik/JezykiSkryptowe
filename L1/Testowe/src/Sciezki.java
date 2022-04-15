import java.io.File;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class Sciezki {
    private static int R = 0;
    private static int d = 0;
    private static int s = 0;
    private static int srt = 0;
    private static int srtopt = 0;

    public static void listFiles(String directory, String tab) {
        File dir = new File(directory);
        File[] files = dir.listFiles();
        ArrayList<File> filesSort = null;

        if (files != null) {
            filesSort = new ArrayList<>(Arrays.asList(files));
        } else {
            return;
        }

        if (srt != 0) {
            if (srtopt != 0) {
                filesSort.sort(Comparator.comparing(File::getName));
            } else {
                filesSort.sort(Comparator.comparing(File::lastModified));
            }
        }

        if (filesSort.size() > 0) {

            for (File file : filesSort) {

                StringBuilder st = new StringBuilder(file.getName());
                boolean isFile = d == 0 || file.isDirectory();

                // pominiecie plików tylko foldery

                if (isFile) { // jest to plik, pominiecie plikow wiec nic nie rób
                    if (s != 0) //
                        st.append("\t" + file.length());
                    System.out.println(tab + st);
                }
                if (R != 0 && file.isDirectory()) // isc rekurencyjnie w folder: wyswietlenie nazwy i wywolanie rekurencyh
                    listFiles(file.getAbsolutePath(), tab + "----");
            }
        }
    }


    public static void main(String[] args) {

        for (int i = 0; i < args.length; i++) {
            if (args[i].equals("-R"))
                R = 1;
            if (args[i].equals("-d"))
                d = 1;
            if (args[i].equals("-s"))
                s = 1;
            if (args[i].equals("--sort")) {
                srt = 1;
                if (args[i + 1].equals("alpha"))
                    srtopt = 1;
                if (args[i + 1].equals("date"))
                    srtopt = 0;
            }
        }
        final String path = System.getProperty("user.dir");
        //System.out.println(path);
        listFiles(path, "");

        //na sztywno
        //listFiles("D:\\MAIN\\CODING\\Sem 4\\JezykiSkryptowe\\L1\\Testowe","");
        //D:\MAIN\CODING\Sem 4\JezykiSkryptowe\L1\Testowe

    }
}
