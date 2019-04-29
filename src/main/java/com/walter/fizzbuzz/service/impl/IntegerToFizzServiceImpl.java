package com.walter.fizzbuzz.service.impl;

import com.walter.fizzbuzz.constant.Constant;
import com.walter.fizzbuzz.service.IntegerToStringService;

/**
 * IntegerToStringService implementation for FIZZ case.
 * @author hp
 */
public class IntegerToFizzServiceImpl implements IntegerToStringService {

	public String transfer(int n) {
		return Constant.FIZZ;
	}

	public boolean support(int n) {
		return 0 == n%3 || String.valueOf(n).contains("3");
	}

}
