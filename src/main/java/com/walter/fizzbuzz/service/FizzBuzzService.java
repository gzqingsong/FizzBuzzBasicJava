package com.walter.fizzbuzz.service;

import java.util.List;

import com.walter.fizzbuzz.enumeration.FizzBuzzStratageEnum;

public interface FizzBuzzService {

	/**
	 * Final output for a given integer n
	 * @param n A given integer
	 * @param integerToStringServiceList An ordered list in which each element represents an method for integer output
	 * @param fizzBuzzStratage The output stratage if a given integer satisfies different output methods
	 * @return
	 */
	public String output(int n, List<IntegerToStringService> integerToStringServiceList, FizzBuzzStratageEnum fizzBuzzStratage);
}
