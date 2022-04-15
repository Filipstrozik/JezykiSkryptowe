import java.util.ArrayList;

public class Avg implements AggregateStrategy{


    @Override
    public double compute(ArrayList<String> lines) {
        double sum = 0.0;
        int cnt = 0;
        for (String line : lines) {
            try {
                sum += Double.parseDouble(line);
            } catch (Exception e) {
                e.printStackTrace();
            }
            cnt++;
        }
        return sum / cnt;
    }
}
