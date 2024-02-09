example1 = """
 import java.util.GregorianCalendar;
import java.util.Scanner;

//What day is today?
public class Main{

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		String[] s = {"","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"};
		while(true){
			int m = sc.nextInt();
			int d = sc.nextInt();
			if(m==0)break;
			GregorianCalendar g = new GregorianCalendar(2004, m-1, d);
			System.out.println(s[g.get(GregorianCalendar.DAY_OF_WEEK)]);
		}
	}
}  
    
"""
example2 ="""
import java.util.GregorianCalendar;
import java.util.Scanner;
public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        String[] day ={"","Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"};
        while (true){
            int a = sc.nextInt();
            int b = sc.nextInt();
            if (a ==0)break;
            GregorianCalendar gre = new GregorianCalendar(2004,a-1,b);
            System.out.println(day[gre.get(GregorianCalendar.DAY_OF_WEEK)]);
        }

    }
}
"""
example3 = """
import java.util.*;

public class Main {
	public static void main(String[] args) throws Exception{
		Scanner scn = new Scanner(System.in);
		int n = scn.nextInt();
		int[] a = new int[n];
		for(int i=0; i<a.length; i++){
			a[i] = scn.nextInt();
		}
      	int[] b = new int[n];
      	for(int i=a.length-1; i>=0; i-=2){
        	System.out.print(a[i]+ " ");
      }
       for(int i=a.length%2; i<a.length; i+=2){
        System.out.print(a[i]+ " ");
      }
	}
}
"""


