#!/usr/bin/env python3
"""
Computer Problem Diagnosis Expert System - Entry Point
"""

from diagnosis_interface import DiagnosisInterface
import sys


def main():
    """Main entry point"""
    try:
        interface = DiagnosisInterface()
        interface.run_diagnosis()
        
        print("\n" + "="*75)
        choice = input("\n🔄 Would you like to diagnose another problem? (y/n): ").strip().lower()
        
        if choice == 'y':
            main()
        else:
            print("\n👋 Thank you for using the Computer Diagnosis Expert System!")
            print("📁 Your diagnosis history is saved in diagnosis_history.json")
            print("\n" + "="*75 + "\n")
    
    except KeyboardInterrupt:
        print("\n\n👋 Diagnosis cancelled. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print("Please try again or contact support.")


if __name__ == "__main__":
    main()