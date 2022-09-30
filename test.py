# test.py

import unittest
import piloadcell as lc

class PiLoadcellTestCases(unittest.TestCase):
  


  def setUp(self):
    self.loadCell = lc(5, 6)
    


  def TestDefaultGain(self):
    self.assertEqual(128, self.loadCell.getGain())



  def TestDefaultBitMSB(self):
    self.assertEqual(True, self.loadCell.getBitMSB())



  def TestDefaultByteMSB(self):
    self.assertEqual(True, self.loadCell.getByteMSB())



  def TestDefaultUnitConversion(self):
    self.assertEqual(1, self.loadCell.getUnitConversion())



  def TestSetGain(self):
    # Verify initial gain set properly
    self.assertEqual(128, self.loadCell.getGain())

    # Test gain set to 64
    self.loadCell.setGain(64)
    self.assertEqual(64, self.loadCell.getGain())

    # Test gain set to 32
    self.loadCell.setGain(32)
    self.assertEqual(32, self.loadCell.getGain())

    # Test invalid gain setpoint
    with self.assertRaises(ValueError):
      self.loadCell.setGain(61)

    # Gain should remain equal to previously set value
    self.assertEqual(32, self.loadCell.getGain())
    


  def TestSetUnitConversion(self):

    # Verify initial unit conversion set properly
    self.assertEqual(1, self.loadCell.getUnitConversion())
    
    # Set new unit conversion
    self.loadCell.setUnitConversion(2)
    self.assertEqual(2, self.loadCell.getUnitConversion())
    
    # Attempt to set invalid unit conversion values
    with self.assertRaises(ValueError):
      self.loadCell.setUnitConversion(0)

    with self.assertRaises(ValueError):
      self.loadCell.setUnitConversion(-1)


  
  def TestCompactBytes(self):

    byteArray1 = [11111111, 11111111, 11111111]
    byteArray2 = [11111111, 00000000, 11111111]

    self.assertEqual(0b111111111111111111111111, self.loadCell.compactBytes(byteArray1))



    def suite():

      suite = unittest.TestSuite()

      # Add tests to suite
      suite.addTest(PiLoadcellTestCases("TestDefaultGain"))
      suite.addTest(PiLoadcellTestCases("TestDefaultBitMSB"))
      suite.addTest(PiLoadcellTestCases("TestDefaultByteMSB"))
      suite.addTest(PiLoadcellTestCases("TestDefaultUnitConversion"))
      suite.addTest(PiLoadcellTestCases("TestSetGain"))
      suite.addTest(PiLoadcellTestCases("TestSetUnitConversion"))
      suite.addTest(PiLoadcellTestCases("TestCompactBytes"))

      return suite

# Run test suite
runner = unittest.TextTestRunner(verbosity=2)
runner.run(PiLoadcellTestCases.suite())