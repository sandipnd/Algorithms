import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.List;
import java.util.Stack;

/*
 * 
 * Definition for an interval.
 * public class Interval {
 *     int start;
 *     int end;
 *     Interval() { start = 0; end = 0; }
 *     Interval(int s, int e) { start = s; end = e; }
 * }
 * Given a collection of intervals, merge all overlapping intervals.

For example,
Given [1,3],[2,6],[8,10],[15,18],
return [1,6],[8,10],[15,18].
 */
public class mergeInterval {

		int start;
		int end;
		mergeInterval() { start = 0; end = 0; }
		mergeInterval(int s, int e) { start = s; end = e; }

	public static boolean compareTwo(mergeInterval o1, mergeInterval o2)	{
		/* if intersect true else false */
		
		if(o2.start < o1.end)
			return true;
		return false;
	}
		
	public static List<mergeInterval> merge(List<mergeInterval> intervals) {
        Stack<mergeInterval> tmpStore = new  Stack<mergeInterval>();
        List<mergeInterval> output = new ArrayList<mergeInterval>();
        
        for(mergeInterval tmp: intervals) {
        	if (tmpStore.isEmpty()) {
        		tmpStore.push(tmp);
        	}
        	else {
        		
        		mergeInterval store = tmpStore.pop();
        		if (compareTwo(store, tmp)) {
        			int end = Math.max(store.end, tmp.end);
        			tmpStore.push(new mergeInterval(store.start,end));
        		}
        		else {
        			tmpStore.push(store);
        			tmpStore.push(tmp);
        			
        		}
        		
        	}

        }
        
        while (!tmpStore.isEmpty()) {
        	output.add(0,tmpStore.pop());
        }
        
		return output;
	}
	
	

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		List<mergeInterval>intervalList = new ArrayList<mergeInterval>();
		intervalList.add(new mergeInterval(1,3));
		intervalList.add(new mergeInterval(2,6));
		intervalList.add(new mergeInterval(8,10));
		intervalList.add(new mergeInterval(15,18));
		intervalList.add(new mergeInterval(1,5));
		
		Collections.sort(intervalList, new Comparator<mergeInterval>(){
		     public int compare(mergeInterval o1, mergeInterval o2){
		         if(o1.start == o2.start)
		             return 0;
		         return o1.start < o2.start ? -1 : 1;
		     }
		});

       for(mergeInterval ival: mergeInterval.merge(intervalList)) {   
    	   System.out.println(ival.start + " : " + ival.end);
       }
	}

}
