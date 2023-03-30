import json
import openai




def chatgpt_request(code1, code2):
    prompt = """
code1: 
import java.util.*;

class Main{
    public static void main(String[] args){
        List<Integer> a = new ArrayList<>();
        Scanner sc = new Scanner(System.in);
        while(sc.hasNextInt()){
            a.add(sc.nextInt());
        }
        a.stream().sorted(Comparator.reverseOrder()).limit(3).forEach(System.out::println);
    }
}

#end of code1

code2:
import java.util.Arrays;
import java.util.Scanner;

public class Main {
	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		int[] m = new int[10];
		
		for(int i=0; i<10; i++) {
			m[i]=sc.nextInt();
		}
		Arrays.sort(m);
		
		for(int i=9; i>=7; i--) {
			System.out.println(m[i]);
		}
	}
}
#end of code 2

code 3:
import java.math.BigInteger;
import java.util.Scanner;

//Numbers
public class Main{

	void run(){
		Scanner sc = new Scanner(System.in);
		int n = sc.nextInt();
		BigInteger b = BigInteger.ONE;
		for(int i=2;i<=n+1;i++)b = b.multiply(BigInteger.valueOf(i));
		System.out.println(b.add(BigInteger.valueOf(2)));
		for(int i=2;i<=n+1;i++)System.out.println(i);
	}
	
	public static void main(String[] args) {
		new Main().run();
	}
}

#end of code 3

# relation shipt:
code1 ^ code2 => 1 (input: a list of ten integers, output: Print the top three numbers in descending order.)
code 1 ^ code 3 => 0 ( different input and outputs)
    
#start of query:
q1 = f"{code1}",
q2 = f"{code2}"

q1 ^ q2 => ?
"""
    openai.api_key = "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"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="user: Hello, AI:",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
    stop=[" AI:"]
)

  
        
with open('java_test_clone.jsonl', 'r') as f:

    # Iterate over each line in the file
    for line in f:

        # Parse the line as JSON
        data = json.loads(line)
        
assert 1 == 1
data = data[0]
code1 = data['code1']
code2 = data['code2']
assert 1 == 1
import os
import openai


# result = chatgpt_request(code1, code2)
assert 1 == 1






"""
code1:
import java.util.*;class Main{public static void main(String[]z){double[]b=new double[8];for(Scanner s=new Scanner(System.in);s.hasNext();System.out.println((f(b[0],b[1],b[4],b[5],b[6],b[7])>0&&f(b[4],b[5],b[0],b[1],b[2],b[3])>0&&f(b[2],b[3],b[6],b[7],b[0],b[1])>0&&f(b[6],b[7],b[2],b[3],b[4],b[5])>0)||(f(b[0],b[1],b[4],b[5],b[6],b[7])<0&&f(b[4],b[5],b[0],b[1],b[2],b[3])<0&&f(b[2],b[3],b[6],b[7],b[0],b[1])<0&&f(b[6],b[7],b[2],b[3],b[4],b[5])<0)?"YES":"NO")){z=s.next().split(",");for(int i=0;i<8;++i)b[i]=new Double(z[i]);}}static double f(double a,double b,double c,double d,double e,double f){return ((d-b)*e+(a-c)*f+c*b-a*d);}}

generate an input and an output for code 1. Now, take code2

code2:
import java.io.*;class Main{public static void main(String[]g)throws Exception{int i,j;boolean f;float l[]=new float[8];BufferedReader B=new BufferedReader(new InputStreamReader(System.in));for(String s;(s=B.readLine())!=null;System.out.println(f?"NO":"YES")){g=s.split(",");f=false;for(j=0;j<2;j++){for(i=0;i<8;i++)l[i]=Float.valueOf(g[(4*j+i)%8]);f|=((l[0]-l[2])*(l[5]-l[1])+(l[1]-l[3])*(l[0]-l[4]))*((l[0]-l[2])*(l[7]-l[1])+(l[1]-l[3])*(l[0]-l[6]))<0;}}}}

If code1 and code2 solve different problems return 0. If the outputs are identical for the same input, return 1; otherwise, return 0". Conclude the result with the "final result is:" so that I can find the result easily.

"""