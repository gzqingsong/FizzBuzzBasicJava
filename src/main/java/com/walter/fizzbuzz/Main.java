package com.walter.fizzbuzz;

import java.util.ArrayList;
import java.util.List;

import com.walter.fizzbuzz.enumeration.FizzBuzzStratageEnum;
import com.walter.fizzbuzz.service.FizzBuzzService;
import com.walter.fizzbuzz.service.IntegerToStringService;
import com.walter.fizzbuzz.service.impl.FizzBuzzServiceImpl;
import com.walter.fizzbuzz.service.impl.IntegerToBuzzServiceImpl;
import com.walter.fizzbuzz.service.impl.IntegerToFizzServiceImpl;

public class Main {

	public static void main(String[] args) {

		int n = 100;
		
		List<IntegerToStringService> integerToStringServiceList = new ArrayList<IntegerToStringService>();
		integerToStringServiceList.add(new IntegerToFizzServiceImpl());
		integerToStringServiceList.add(new IntegerToBuzzServiceImpl());
		
		FizzBuzzService fizzBuzzService = new FizzBuzzServiceImpl();
		
		for(int i=1; i<=n; i++) {
			String result = fizzBuzzService.output(i, integerToStringServiceList, FizzBuzzStratageEnum.APPEND_ALL_ASC);
			System.out.println(result);
		}
		
	}

}
