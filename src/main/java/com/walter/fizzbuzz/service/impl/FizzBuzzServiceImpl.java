package com.walter.fizzbuzz.service.impl;

import java.util.List;

import com.walter.fizzbuzz.enumeration.FizzBuzzStratageEnum;
import com.walter.fizzbuzz.exception.FizzBuzzException;
import com.walter.fizzbuzz.service.IntegerToStringService;
import com.walter.fizzbuzz.service.FizzBuzzService;

public class FizzBuzzServiceImpl implements FizzBuzzService {

	public String output(int n, List<IntegerToStringService> integerToStringServiceList,
			FizzBuzzStratageEnum fizzBuzzStratage) {

		StringBuffer result = new StringBuffer();

		if (FizzBuzzStratageEnum.APPEND_ALL_ASC.getCode().equals(fizzBuzzStratage.getCode())) {
			for (IntegerToStringService calcService : integerToStringServiceList) {
				if (calcService.support(n)) {
					result.append(calcService.transfer(n));
				}
			}

			if (0 == result.length()) {
				result.append(String.valueOf(n));
			}
		} else {
			throw new FizzBuzzException(
					String.format("Unsupported FizzBuzzStratageEnum(%s)", fizzBuzzStratage.getCode()));
		}

		return result.toString();
	}
}
