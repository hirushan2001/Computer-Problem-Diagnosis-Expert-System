#!/usr/bin/env python3
"""
Computer Problem Diagnosis Expert System
Interactive terminal-based expert system for diagnosing computer problems
Author: IT Student
Date: October 2024
"""

from knowledge_base import ComputerDiagnosisSystem, save_diagnosis, Fact
from datetime import datetime
import sys
import os

class DiagnosisInterface:
    def __init__(self):
        self.engine = ComputerDiagnosisSystem()
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
                print("\n\n👋 Diagnosis cancelled. Goodbye!")
                sys.exit(0)
    
    def run_diagnosis(self):
        """Main diagnosis flow"""
        self.print_header()
        self.clear_screen()
        
        print("\n" + "="*75)
        print(" "*25 + "DIAGNOSIS QUESTIONNAIRE")
        print("="*75 + "\n")
        
        # Question 1: Main category
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
        
        # Based on main category, ask specific questions
        if issue == "Power/Boot Problems":
            self.diagnose_power_boot()
        elif issue == "Performance Issues (Slow/Freezing)":
            self.diagnose_performance()
        elif issue == "Blue Screen of Death (BSOD)":
            self.diagnose_bsod()
        elif issue == "Network/Internet Problems":
            self.diagnose_network()
        elif issue == "Application Issues":
            self.diagnose_applications()
        elif issue == "Peripheral Devices (Printer/USB/Keyboard/Mouse)":
            self.diagnose_peripherals()
        elif issue == "Audio/Sound Problems":
            self.diagnose_audio()
        elif issue == "Security Concerns (Malware/Virus)":
            self.diagnose_security()
        elif issue == "Storage/Disk Problems":
            self.diagnose_storage()
        elif issue == "Windows Update Issues":
            self.diagnose_windows_update()
        elif issue == "Display Problems":
            self.diagnose_display()
    
    def diagnose_power_boot(self):
        """Diagnose power and boot issues"""
        status = self.get_choice(
            "What is the power status?",
            ["Computer won't turn on at all", "Computer turns on but won't boot", "Computer shows BIOS then stops"]
        )
        
        if status == "Computer won't turn on at all":
            self.user_facts['power_status'] = 'not_turning_on'
            
            cable = self.get_choice("Is the power cable connected properly?", ["Yes", "No"])
            self.user_facts['power_cable'] = 'connected' if cable == "Yes" else 'disconnected'
            
            if cable == "Yes":
                outlet = self.get_choice("Is the power outlet working? (Test with another device)", ["Yes", "No"])
                self.user_facts['outlet_working'] = 'yes' if outlet == "Yes" else 'no'
                
                if outlet == "Yes":
                    lights = self.get_choice(
                        "When you press the power button, do any lights turn on?",
                        ["No lights at all", "Lights turn on", "Fans spin but no display"]
                    )
                    
                    if lights == "No lights at all":
                        self.user_facts['lights'] = 'none'
                    elif lights == "Lights turn on":
                        self.user_facts['lights'] = 'on'
                        self.user_facts['display'] = 'no_signal'
        
        elif status == "Computer turns on but won't boot":
            self.user_facts['power_status'] = 'turning_on'
            
            boot = self.get_choice(
                "What stage does it reach?",
                ["No BIOS screen", "BIOS shows then stops", "Searching for boot device"]
            )
            
            if boot == "No BIOS screen":
                self.user_facts['boot_stage'] = 'no_bios'
            elif boot == "BIOS shows then stops":
                self.user_facts['boot_stage'] = 'bios_shows'
                beep = self.get_choice(
                    "Do you hear any beep codes?",
                    ["No beeps", "1 long, 2 short beeps", "Continuous beeping"]
                )
                
                if beep == "1 long, 2 short beeps":
                    self.user_facts['beep_code'] = '1_long_2_short'
                elif beep == "Continuous beeping":
                    self.user_facts['beep_code'] = 'continuous'
            elif boot == "Searching for boot device":
                self.user_facts['boot_stage'] = 'bios_shows'
                self.user_facts['boot_device'] = 'not_found'
        
        # Run engine with collected facts
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
        else:
            self.print_diagnosis(
                "Unable to diagnose specific issue",
                "Try basic troubleshooting steps or consult a technician",
                "medium"
            )
    
    def diagnose_performance(self):
        """Diagnose performance issues"""
        self.user_facts['issue_category'] = 'performance'
        
        symptom = self.get_choice(
            "What performance issue are you experiencing?",
            ["Very slow performance", "Computer freezing/hanging", "Random shutdowns", "Overheating"]
        )
        
        if symptom == "Very slow performance":
            self.user_facts['symptom'] = 'very_slow'
            
            disk = self.get_choice("What type of drive do you have?", ["HDD (Hard Disk)", "SSD (Solid State)", "Don't know"])
            if disk == "HDD (Hard Disk)":
                self.user_facts['disk_type'] = 'hdd'
                health = self.get_choice(
                    "Have you checked disk health? Any warnings?",
                    ["Yes, shows warnings", "No warnings", "Haven't checked"]
                )
                if health == "Yes, shows warnings":
                    self.user_facts['disk_health'] = 'poor'
            
            cpu = self.get_choice(
                "Check Task Manager - Is CPU usage constantly high (>80%)?",
                ["Yes", "No"]
            )
            if cpu == "Yes":
                self.user_facts['cpu_usage'] = 'high'
                process = self.get_choice(
                    "Can you identify which program is using CPU?",
                    ["Yes, I know the program", "No, unknown process", "Multiple processes"]
                )
                if process == "No, unknown process":
                    self.user_facts['process'] = 'unknown'
            
            ram = self.get_choice(
                "Check Task Manager - Memory (RAM) usage high?",
                ["Yes, >80%", "No, <50%"]
            )
            if ram == "Yes, >80%":
                self.user_facts['ram_usage'] = 'high'
                available = self.get_choice("How much RAM do you have?", ["4GB or less", "8GB", "16GB or more"])
                if available in ["4GB or less", "8GB"]:
                    self.user_facts['available_ram'] = 'low'
        
        elif symptom == "Overheating":
            self.user_facts['temperature'] = 'very_high'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_bsod(self):
        """Diagnose Blue Screen issues"""
        self.user_facts['issue_category'] = 'bsod'
        
        error = self.get_choice(
            "What error code does the blue screen show?",
            [
                "DRIVER_IRQL_NOT_LESS_OR_EQUAL",
                "MEMORY_MANAGEMENT",
                "KERNEL_DATA_INPAGE_ERROR",
                "SYSTEM_SERVICE_EXCEPTION",
                "PAGE_FAULT_IN_NONPAGED_AREA",
                "Other/Don't know"
            ]
        )
        
        if error != "Other/Don't know":
            self.user_facts['error_code'] = error.replace("_", "_")
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_network(self):
        """Diagnose network issues"""
        self.user_facts['issue_category'] = 'network'
        
        symptom = self.get_choice(
            "What is the network problem?",
            [
                "No internet connection",
                "Very slow internet",
                "Can't connect to WiFi",
                "Intermittent connection (keeps dropping)",
                "Connected but no access"
            ]
        )
        
        if symptom == "No internet connection":
            self.user_facts['symptom'] = 'no_internet'
            
            other = self.get_choice(
                "Are other devices (phone/tablet) working on same network?",
                ["Yes, they work", "No, nothing works"]
            )
            self.user_facts['other_devices'] = 'working' if other == "Yes, they work" else 'not_working'
        
        elif symptom == "Very slow internet":
            self.user_facts['symptom'] = 'slow_internet'
            
            conn_type = self.get_choice("Are you using WiFi or Ethernet cable?", ["WiFi", "Ethernet"])
            self.user_facts['connection'] = conn_type.lower()
            
            if conn_type == "WiFi":
                signal = self.get_choice("Is WiFi signal strength good?", ["Weak signal (1-2 bars)", "Good signal (3-4 bars)"])
                self.user_facts['signal'] = 'weak' if "Weak" in signal else 'good'
        
        elif symptom == "Can't connect to WiFi":
            self.user_facts['symptom'] = 'cannot_connect'
            self.user_facts['connection'] = 'wifi'
            
            visible = self.get_choice("Can you see your WiFi network in the list?", ["Yes", "No"])
            self.user_facts['network_visible'] = 'yes' if visible == "Yes" else 'no'
        
        elif symptom == "Connected but no access":
            dns = self.get_choice(
                "Can you open websites if you type IP address like 8.8.8.8?",
                ["Yes, IP works", "No, nothing works"]
            )
            if dns == "Yes, IP works":
                self.user_facts['dns_working'] = 'no'
                self.user_facts['can_ping_ip'] = 'yes'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_applications(self):
        """Diagnose application issues"""
        self.user_facts['issue_category'] = 'application'
        
        symptom = self.get_choice(
            "What is the application problem?",
            ["Programs crash frequently", "Can't install software", "Program won't start"]
        )
        
        if symptom == "Programs crash frequently":
            self.user_facts['symptom'] = 'crashes'
            
            which = self.get_choice(
                "Which programs crash?",
                ["One specific program", "Multiple/all programs"]
            )
            self.user_facts['which_apps'] = 'specific' if which == "One specific program" else 'all'
        
        elif symptom == "Can't install software":
            self.user_facts['symptom'] = 'wont_install'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_peripherals(self):
        """Diagnose peripheral issues"""
        self.user_facts['issue_category'] = 'peripheral'
        
        device = self.get_choice(
            "Which device has a problem?",
            ["Printer", "USB Device (flash drive, external HDD)", "Keyboard/Mouse"]
        )
        
        if device == "Printer":
            self.user_facts['device'] = 'printer'
            symptom = self.get_choice(
                "What is the printer issue?",
                ["Not detected/found", "Print queue stuck", "Poor print quality"]
            )
            
            if symptom == "Not detected/found":
                self.user_facts['symptom'] = 'not_detected'
            elif symptom == "Print queue stuck":
                self.user_facts['symptom'] = 'queue_stuck'
        
        elif device == "USB Device (flash drive, external HDD)":
            self.user_facts['device'] = 'usb'
            symptom = self.get_choice(
                "What is the USB issue?",
                ["Not recognized/detected", "Keeps disconnecting", "Very slow"]
            )
            
            if symptom == "Not recognized/detected":
                self.user_facts['symptom'] = 'not_recognized'
            elif symptom == "Keeps disconnecting":
                self.user_facts['symptom'] = 'keeps_disconnecting'
        
        elif device == "Keyboard/Mouse":
            self.user_facts['device'] = 'keyboard_mouse'
            conn = self.get_choice("Is it wired or wireless?", ["Wired (USB)", "Wireless"])
            self.user_facts['connection'] = 'wireless' if conn == "Wireless" else 'wired'
            self.user_facts['symptom'] = 'not_working'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_audio(self):
        """Diagnose audio issues"""
        self.user_facts['issue_category'] = 'audio'
        
        symptom = self.get_choice(
            "What is the audio problem?",
            ["No sound at all", "Crackling/distorted sound", "Sound from wrong device"]
        )
        
        if symptom == "No sound at all":
            self.user_facts['symptom'] = 'no_sound'
            
            detected = self.get_choice(
                "Is audio device shown in Sound settings?",
                ["Yes, I see it", "No, not listed"]
            )
            self.user_facts['device_detected'] = 'yes' if detected == "Yes, I see it" else 'no'
            
            if detected == "Yes, I see it":
                muted = self.get_choice("Is it muted or volume at 0?", ["No, volume is up", "Yes, was muted"])
                self.user_facts['muted'] = 'no' if muted == "No, volume is up" else 'yes'
        
        elif symptom == "Crackling/distorted sound":
            self.user_facts['symptom'] = 'crackling'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_security(self):
        """Diagnose security issues"""
        self.user_facts['issue_category'] = 'security'
        
        symptom = self.get_choice(
            "What security concern do you have?",
            [
                "Suspected malware/virus",
                "Pop-up ads everywhere",
                "Browser redirects to strange sites",
                "Files encrypted (ransomware)",
                "Unknown programs running"
            ]
        )
        
        if symptom in ["Suspected malware/virus", "Pop-up ads everywhere", "Unknown programs running"]:
            self.user_facts['symptom'] = 'malware_suspected'
            
            if symptom == "Pop-up ads everywhere":
                self.user_facts['signs'] = 'popup_ads'
            elif symptom == "Unknown programs running":
                self.user_facts['signs'] = 'unknown_programs'
        
        elif symptom == "Browser redirects to strange sites":
            self.user_facts['symptom'] = 'malware_suspected'
            self.user_facts['signs'] = 'browser_redirects'
        
        elif symptom == "Files encrypted (ransomware)":
            self.user_facts['symptom'] = 'ransomware'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_storage(self):
        """Diagnose storage issues"""
        self.user_facts['issue_category'] = 'storage'
        
        symptom = self.get_choice(
            "What is the storage problem?",
            ["Disk full/low space", "External drive not showing", "Drive errors/warnings", "Very slow drive"]
        )
        
        if symptom == "Disk full/low space":
            self.user_facts['symptom'] = 'disk_full'
        elif symptom == "External drive not showing":
            self.user_facts['symptom'] = 'external_not_showing'
        elif symptom == "Drive errors/warnings":
            self.user_facts['symptom'] = 'drive_errors'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_windows_update(self):
        """Diagnose Windows Update issues"""
        self.user_facts['issue_category'] = 'windows_update'
        
        symptom = self.get_choice(
            "What is the Windows Update problem?",
            ["Update keeps failing", "Update stuck/frozen", "Update taking too long"]
        )
        
        if symptom == "Update keeps failing":
            self.user_facts['symptom'] = 'update_failing'
        elif symptom in ["Update stuck/frozen", "Update taking too long"]:
            self.user_facts['symptom'] = 'update_stuck'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])
    
    def diagnose_display(self):
        """Diagnose display issues"""
        self.user_facts['issue_category'] = 'display'
        
        symptom = self.get_choice(
            "What is the display problem?",
            ["No display/black screen", "Screen flickering", "Wrong resolution", "Display colors wrong"]
        )
        
        if symptom == "No display/black screen":
            self.user_facts['symptom'] = 'no_display'
            power = self.get_choice("Is the computer powered on (lights/fans)?", ["Yes", "No"])
            self.user_facts['power_on'] = 'yes' if power == "Yes" else 'no'
        
        elif symptom == "Screen flickering":
            self.user_facts['symptom'] = 'flickering'
        
        # Run engine
        self.engine.reset()
        for key, value in self.user_facts.items():
            self.engine.declare(Fact(**{key: value}))
        self.engine.run()
        
        if self.engine.diagnosis_result:
            result = self.engine.diagnosis_result
            self.print_diagnosis(result['diagnosis'], result['solution'], result['severity'])


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