import java.util.ArrayList;

public class Variance implements AggregateStrategy{

    @Override
    public double compute(ArrayList<String> lines) {
        double avg = new Avg().compute(lines);
        double sum = 0.0;
        int cnt = 0;
        for (String line : lines) {
            sum += Math.pow((Double.parseDouble(line) - avg), 2);
            cnt++;
        }
        return sum / cnt;
    }
}
