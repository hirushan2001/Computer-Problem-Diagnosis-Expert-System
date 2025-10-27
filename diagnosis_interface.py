"""
Diagnosis Interface - Handles user interaction and display
"""

from knowledge_base import ComputerDiagnosisSystem, save_diagnosis
from diagnosis_questions import DiagnosisQuestions
from experta import Fact
from datetime import datetime
import os


class DiagnosisInterface:
    def __init__(self):
        self.engine = ComputerDiagnosisSystem()
        self.questions = DiagnosisQuestions()
        self.user_facts = {}
        self.session_start = datetime.now()
        
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def print_header(self):
        """Print welcome header"""
        self.clear_screen()
        print("\n" + "="*75)
        print(" "*15 + "COMPUTER PROBLEM DIAGNOSIS EXPERT SYSTEM")
        print("="*75)
        print("\n🖥️  Welcome! This expert system will help diagnose your computer problems.")
        print("\n📋 System covers:")
        print("   • Hardware Issues    • Software Issues    • Network Problems")
        print("   • BSOD Errors        • Boot Problems      • Performance Issues")
        print("   • Peripheral Devices • Audio Issues       • Security Concerns")
        print("   • Storage Problems   • Windows Updates    • Display Issues")
        print("\n" + "="*75 + "\n")
        input("Press Enter to start diagnosis...")
    
    def print_diagnosis(self, diagnosis, solution, severity):
        """Display diagnosis result"""
        self.clear_screen()
        print("\n" + "="*75)
        print(" "*25 + "DIAGNOSIS RESULT")
        print("="*75)
        
        severity_display = {
            'critical': '🔴 CRITICAL - URGENT ACTION REQUIRED',
            'high': '🟠 HIGH - Address Soon',
            'medium': '🟡 MEDIUM - Should Fix',
            'low': '🟢 LOW - Minor Issue'
        }
        
        print(f"\n⚠️  Severity: {severity_display.get(severity, '⚪ UNKNOWN')}")
        print(f"\n🔍 Diagnosis:\n   {diagnosis}")
        print(f"\n💡 Recommended Solution:")
        
        for line in solution.split('\n'):
            print(f"   {line}")
        
        print("\n" + "="*75)
        
        # Save to history
        diagnosis_data = {
            'timestamp': self.session_start.isoformat(),
            'diagnosis': diagnosis,
            'solution': solution,
            'severity': severity,
            'facts': self.user_facts
        }
        save_diagnosis(diagnosis_data)
        print("\n✅ Diagnosis saved to history (diagnosis_history.json)")
    
    def get_choice(self, question, options):
        """Get user input with validation"""
        print(f"\n❓ {question}")
        for i, option in enumerate(options, 1):
            print(f"   {i}. {option}")
        
        while True:
            try:
                choice = input("\n👉 Your choice (enter number): ").strip()
                choice_num = int(choice)
                if 1 <= choice_num <= len(options):
                    return options[choice_num - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(options)}")
            except ValueError:
                print("❌ Please enter a valid number")
            except KeyboardInterrupt:
                raise
    
    def run_diagnosis(self):
        """Main diagnosis flow"""
        self.print_header()
        self.clear_screen()
        
        print("\n" + "="*75)
        print(" "*25 + "DIAGNOSIS QUESTIONNAIRE")
        print("="*75 + "\n")
        
        # Get main category
        issue = self.get_choice(
            "What type of issue are you experiencing?",
            [
                "Power/Boot Problems",
                "Performance Issues (Slow/Freezing)",
                "Blue Screen of Death (BSOD)",
                "Network/Internet Problems",
                "Application Issues",
                "Peripheral Devices (Printer/USB/Keyboard/Mouse)",
                "Audio/Sound Problems",
                "Security Concerns (Malware/Virus)",
                "Storage/Disk Problems",
                "Windows Update Issues",
                "Display Problems"
            ]
        )
        
        # Route to appropriate diagnosis method
        diagnosis_methods = {
            "Power/Boot Problems": self.questions.ask_power_boot,
            "Performance Issues (Slow/Freezing)": self.questions.ask_performance,
            "Blue Screen of Death (BSOD)": self.questions.ask_bsod,
            "Network/Internet Problems": self.questions.ask_network,
            "Application Issues": self.questions.ask_applications,
            "Peripheral Devices (Printer/USB/Keyboard/Mouse)": self.questions.ask_peripherals,
            "Audio/Sound Problems": self.questions.ask_audio,
            "Security Concerns (Malware/Virus)": self.questions.ask_security,
            "Storage/Disk Problems": self.questions.ask_storage,
            "Windows Update Issues": self.questions.ask_windows_update,
            "Display Problems": self.questions.ask_display
        }
        
        # Get facts from questions
        self.user_facts = diagnosis_methods[issue](self.get_choice)
        
        # Run expert system
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        # Display result
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
        else:
            self.print_diagnosis(
                "Unable to diagnose specific issue",
                "Try basic troubleshooting steps or consult a technician",
                "medium"
            )