import java.util.Map;


public class PokazWszystkie {

    public static void main(String[] args) {

        Map<String, String> env = System.getenv();
        env.forEach((k,v) -> System.out.print(k.toUpperCase() + "=" + v +" "));
        System.out.println();
        for(String s: args){
            System.out.print(s+" ");
        }
    }
}
