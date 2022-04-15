import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Objects;
import java.util.stream.Collectors;

public class PokazPodobne {

    public static void main(String[] args) {
        int silent = 0;

        if (args.length != 0) { // sprawdz czy jest silent
            silent = args[0].equals("/S") ? 1 : 0; // jezeli tak to bedziemy miec taki tryb
        } else {
            args = new String[1]; // nie ma zadnych argumentow
            args[0] = "";
        }

        for (int i = silent; i < Objects.requireNonNull(args).length; i++) {

            System.out.println("Zmienne srodowiskowe:");

            Map<String, String> env = System.getenv();
            String arg = args[i]; // argumrnt do szukania zaleznie czy silent
            LinkedHashMap<String, String> collection =
                    env.entrySet().stream()
                            .filter(x -> x.getKey().contains(arg))
                            .sorted(Map.Entry.comparingByKey(Comparator.reverseOrder()))
                            .collect(Collectors.toMap(
                                    Map.Entry::getKey,
                                    Map.Entry::getValue,
                                    (oldValue, newValue) -> oldValue,
                                    LinkedHashMap::new)
                            );
            if (collection.isEmpty()) {
                if (silent == 0)
                    System.out.println(arg.toUpperCase() + " = NONE");
            } else { // formatowanie
                collection.forEach((k, v) -> {
                            String[] arrayValues = v.split(";");
                            System.out.println(k.toUpperCase() + " = " + arrayValues[0].toLowerCase());
                            for (int j = 1; j < arrayValues.length; j++) {
                                String a = arrayValues[j];
                                System.out.println("\t" + a.toLowerCase());
                            }
                            System.out.println("-------------------------");
                        }
                );
            }
        }
    }
}