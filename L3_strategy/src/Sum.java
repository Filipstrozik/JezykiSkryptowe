import java.util.ArrayList;

public class Sum implements AggregateStrategy{

    @Override
    public double compute(ArrayList<String> lines) {
        double sum = 0.0;
        for (String line : lines) {
            sum += Double.parseDouble(line);
        }
        return sum;
    }
}
