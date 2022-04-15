import java.util.*;
import java.util.stream.Collectors;

public class KodPowrotu {

    public static void main(String[] args) {
        Map<String, Integer> map = Arrays.stream(args).collect(Collectors.toMap(e -> e, e -> 0));
        if (map.size() == 0) {
            System.exit(0);
        }
        Scanner sc = new Scanner(System.in); // scaner standardowe wejscie
        while (sc.hasNext()) {
            String word = sc.next();
            if (map.containsKey(word)) {
                map.put(word, map.get(word) + 1);
            }
        }

        Map.Entry<String, Integer> maxEntry = Collections.max(map.entrySet(), Map.Entry.comparingByValue());
        if (maxEntry.getValue() == 0) {
            System.exit(0); // nie wystapuje parametr ani razu
        }

        for (int i = 0; i < args.length; i++) {
            if (args[i].equals(maxEntry.getKey())) {
                System.exit(i + 1);
            }
        }
    }
}
