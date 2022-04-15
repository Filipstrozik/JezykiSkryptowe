import java.util.ArrayList;

public class Count implements AggregateStrategy{

    @Override
    public double compute(ArrayList<String> lines) {
        return lines.size();
    }
}
