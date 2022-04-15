import java.util.ArrayList;
import java.util.Comparator;

public class Median implements AggregateStrategy{

    @Override
    public double compute(ArrayList<String> lines) {
        lines.sort(Comparator.comparing(String::valueOf));
        if (lines.size() % 2 == 0) {
            int i = lines.size() / 2;
            double a = Double.parseDouble(lines.get(i));
            double b = Double.parseDouble(lines.get(i + 1));
            return ((a + b) / 2.0);
        } else {
            return Double.parseDouble(lines.get(lines.size() / 2));
        }
    }
}
