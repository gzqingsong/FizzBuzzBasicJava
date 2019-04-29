package com.walter.fizzbuzz.testsuite;

import org.junit.runner.RunWith;
import org.junit.runners.Suite;
import org.junit.runners.Suite.SuiteClasses;

import com.walter.fizzbuzz.service.impl.FizzBuzzServiceImplTest;
import com.walter.fizzbuzz.service.impl.IntegerToBuzzServiceImplTest;
import com.walter.fizzbuzz.service.impl.IntegerToFizzServiceImplTest;

@RunWith(Suite.class)
@SuiteClasses({
	IntegerToFizzServiceImplTest.class,
	IntegerToBuzzServiceImplTest.class,
	FizzBuzzServiceImplTest.class
})
public class FizzBuzzSuiteTest {

}
