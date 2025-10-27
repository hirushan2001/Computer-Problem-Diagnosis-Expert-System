"""
Diagnosis Questions - All question logic separated
"""


class DiagnosisQuestions:
    """Handles all diagnostic questions for different categories"""
    
    def ask_power_boot(self, get_choice):
        """Ask power/boot related questions"""
        facts = {}
        
        status = get_choice(
            "What is the power status?",
            ["Computer won't turn on at all", "Computer turns on but won't boot", "Computer shows BIOS then stops"]
        )
        
        if status == "Computer won't turn on at all":
            facts['power_status'] = 'not_turning_on'
            
            cable = get_choice("Is the power cable connected properly?", ["Yes", "No"])
            facts['power_cable'] = 'connected' if cable == "Yes" else 'disconnected'
            
            if cable == "Yes":
                outlet = get_choice("Is the power outlet working? (Test with another device)", ["Yes", "No"])
                facts['outlet_working'] = 'yes' if outlet == "Yes" else 'no'
                
                if outlet == "Yes":
                    lights = get_choice(
                        "When you press the power button, do any lights turn on?",
                        ["No lights at all", "Lights turn on", "Fans spin but no display"]
                    )
                    
                    if lights == "No lights at all":
                        facts['lights'] = 'none'
                    elif lights == "Lights turn on":
                        facts['lights'] = 'on'
                        facts['display'] = 'no_signal'
        
        elif status == "Computer turns on but won't boot":
            facts['power_status'] = 'turning_on'
            
            boot = get_choice(
                "What stage does it reach?",
                ["No BIOS screen", "BIOS shows then stops", "Searching for boot device"]
            )
            
            if boot == "No BIOS screen":
                facts['boot_stage'] = 'no_bios'
            elif boot == "BIOS shows then stops":
                facts['boot_stage'] = 'bios_shows'
                beep = get_choice(
                    "Do you hear any beep codes?",
                    ["No beeps", "1 long, 2 short beeps", "Continuous beeping"]
                )
                
                if beep == "1 long, 2 short beeps":
                    facts['beep_code'] = '1_long_2_short'
                elif beep == "Continuous beeping":
                    facts['beep_code'] = 'continuous'
            elif boot == "Searching for boot device":
                facts['boot_stage'] = 'bios_shows'
                facts['boot_device'] = 'not_found'
        
        return facts
    
    def ask_performance(self, get_choice):
        """Ask performance related questions"""
        facts = {'issue_category': 'performance'}
        
        symptom = get_choice(
            "What performance issue are you experiencing?",
            ["Very slow performance", "Computer freezing/hanging", "Random shutdowns", "Overheating"]
        )
        
        if symptom == "Very slow performance":
            facts['symptom'] = 'very_slow'
            
            disk = get_choice("What type of drive do you have?", ["HDD (Hard Disk)", "SSD (Solid State)", "Don't know"])
            if disk == "HDD (Hard Disk)":
                facts['disk_type'] = 'hdd'
                health = get_choice(
                    "Have you checked disk health? Any warnings?",
                    ["Yes, shows warnings", "No warnings", "Haven't checked"]
                )
                if health == "Yes, shows warnings":
                    facts['disk_health'] = 'poor'
            
            cpu = get_choice("Check Task Manager - Is CPU usage constantly high (>80%)?", ["Yes", "No"])
            if cpu == "Yes":
                facts['cpu_usage'] = 'high'
                process = get_choice(
                    "Can you identify which program is using CPU?",
                    ["Yes, I know the program", "No, unknown process", "Multiple processes"]
                )
                if process == "No, unknown process":
                    facts['process'] = 'unknown'
            
            ram = get_choice("Check Task Manager - Memory (RAM) usage high?", ["Yes, >80%", "No, <50%"])
            if ram == "Yes, >80%":
                facts['ram_usage'] = 'high'
                available = get_choice("How much RAM do you have?", ["4GB or less", "8GB", "16GB or more"])
                if available in ["4GB or less", "8GB"]:
                    facts['available_ram'] = 'low'
        
        elif symptom == "Overheating":
            facts['temperature'] = 'very_high'
        
        return facts
    
    def ask_bsod(self, get_choice):
        """Ask BSOD related questions"""
        facts = {'issue_category': 'bsod'}
        
        error = get_choice(
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
            facts['error_code'] = error
        
        return facts
    
    def ask_network(self, get_choice):
        """Ask network related questions"""
        facts = {'issue_category': 'network'}
        
        symptom = get_choice(
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
            facts['symptom'] = 'no_internet'
            other = get_choice(
                "Are other devices (phone/tablet) working on same network?",
                ["Yes, they work", "No, nothing works"]
            )
            facts['other_devices'] = 'working' if other == "Yes, they work" else 'not_working'
        
        elif symptom == "Very slow internet":
            facts['symptom'] = 'slow_internet'
            conn_type = get_choice("Are you using WiFi or Ethernet cable?", ["WiFi", "Ethernet"])
            facts['connection'] = conn_type.lower()
            
            if conn_type == "WiFi":
                signal = get_choice("Is WiFi signal strength good?", ["Weak signal (1-2 bars)", "Good signal (3-4 bars)"])
                facts['signal'] = 'weak' if "Weak" in signal else 'good'
        
        elif symptom == "Can't connect to WiFi":
            facts['symptom'] = 'cannot_connect'
            facts['connection'] = 'wifi'
            visible = get_choice("Can you see your WiFi network in the list?", ["Yes", "No"])
            facts['network_visible'] = 'yes' if visible == "Yes" else 'no'
        
        elif symptom == "Connected but no access":
            dns = get_choice(
                "Can you open websites if you type IP address like 8.8.8.8?",
                ["Yes, IP works", "No, nothing works"]
            )
            if dns == "Yes, IP works":
                facts['dns_working'] = 'no'
                facts['can_ping_ip'] = 'yes'
        
        return facts
    
    def ask_applications(self, get_choice):
        """Ask application related questions"""
        facts = {'issue_category': 'application'}
        
        symptom = get_choice(
            "What is the application problem?",
            ["Programs crash frequently", "Can't install software", "Program won't start"]
        )
        
        if symptom == "Programs crash frequently":
            facts['symptom'] = 'crashes'
            which = get_choice("Which programs crash?", ["One specific program", "Multiple/all programs"])
            facts['which_apps'] = 'specific' if which == "One specific program" else 'all'
        
        elif symptom == "Can't install software":
            facts['symptom'] = 'wont_install'
        
        return facts
    
    def ask_peripherals(self, get_choice):
        """Ask peripheral related questions"""
        facts = {'issue_category': 'peripheral'}
        
        device = get_choice(
            "Which device has a problem?",
            ["Printer", "USB Device (flash drive, external HDD)", "Keyboard/Mouse"]
        )
        
        if device == "Printer":
            facts['device'] = 'printer'
            symptom = get_choice(
                "What is the printer issue?",
                ["Not detected/found", "Print queue stuck", "Poor print quality"]
            )
            
            if symptom == "Not detected/found":
                facts['symptom'] = 'not_detected'
            elif symptom == "Print queue stuck":
                facts['symptom'] = 'queue_stuck'
        
        elif device == "USB Device (flash drive, external HDD)":
            facts['device'] = 'usb'
            symptom = get_choice(
                "What is the USB issue?",
                ["Not recognized/detected", "Keeps disconnecting", "Very slow"]
            )
            
            if symptom == "Not recognized/detected":
                facts['symptom'] = 'not_recognized'
            elif symptom == "Keeps disconnecting":
                facts['symptom'] = 'keeps_disconnecting'
        
        elif device == "Keyboard/Mouse":
            facts['device'] = 'keyboard_mouse'
            conn = get_choice("Is it wired or wireless?", ["Wired (USB)", "Wireless"])
            facts['connection'] = 'wireless' if conn == "Wireless" else 'wired'
            facts['symptom'] = 'not_working'
        
        return facts
    
    def ask_audio(self, get_choice):
        """Ask audio related questions"""
        facts = {'issue_category': 'audio'}
        
        symptom = get_choice(
            "What is the audio problem?",
            ["No sound at all", "Crackling/distorted sound", "Sound from wrong device"]
        )
        
        if symptom == "No sound at all":
            facts['symptom'] = 'no_sound'
            detected = get_choice("Is audio device shown in Sound settings?", ["Yes, I see it", "No, not listed"])
            facts['device_detected'] = 'yes' if detected == "Yes, I see it" else 'no'
            
            if detected == "Yes, I see it":
                muted = get_choice("Is it muted or volume at 0?", ["No, volume is up", "Yes, was muted"])
                facts['muted'] = 'no' if muted == "No, volume is up" else 'yes'
        
        elif symptom == "Crackling/distorted sound":
            facts['symptom'] = 'crackling'
        
        return facts
    
    def ask_security(self, get_choice):
        """Ask security related questions"""
        facts = {'issue_category': 'security'}
        
        symptom = get_choice(
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
            facts['symptom'] = 'malware_suspected'
            
            if symptom == "Pop-up ads everywhere":
                facts['signs'] = 'popup_ads'
            elif symptom == "Unknown programs running":
                facts['signs'] = 'unknown_programs'
        
        elif symptom == "Browser redirects to strange sites":
            facts['symptom'] = 'malware_suspected'
            facts['signs'] = 'browser_redirects'
        
        elif symptom == "Files encrypted (ransomware)":
            facts['symptom'] = 'ransomware'
        
        return facts
    
    def ask_storage(self, get_choice):
        """Ask storage related questions"""
        facts = {'issue_category': 'storage'}
        
        symptom = get_choice(
            "What is the storage problem?",
            ["Disk full/low space", "External drive not showing", "Drive errors/warnings", "Very slow drive"]
        )
        
        if symptom == "Disk full/low space":
            facts['symptom'] = 'disk_full'
        elif symptom == "External drive not showing":
            facts['symptom'] = 'external_not_showing'
        elif symptom == "Drive errors/warnings":
            facts['symptom'] = 'drive_errors'
        
        return facts
    
    def ask_windows_update(self, get_choice):
        """Ask Windows Update related questions"""
        facts = {'issue_category': 'windows_update'}
        
        symptom = get_choice(
            "What is the Windows Update problem?",
            ["Update keeps failing", "Update stuck/frozen", "Update taking too long"]
        )
        
        if symptom == "Update keeps failing":
            facts['symptom'] = 'update_failing'
        elif symptom in ["Update stuck/frozen", "Update taking too long"]:
            facts['symptom'] = 'update_stuck'
        
        return facts
    
    def ask_display(self, get_choice):
        """Ask display related questions"""
        facts = {'issue_category': 'display'}
        
        symptom = get_choice(
            "What is the display problem?",
            ["No display/black screen", "Screen flickering", "Wrong resolution", "Display colors wrong"]
        )
        
        if symptom == "No display/black screen":
            facts['symptom'] = 'no_display'
            power = get_choice("Is the computer powered on (lights/fans)?", ["Yes", "No"])
            facts['power_on'] = 'yes' if power == "Yes" else 'no'
        
        elif symptom == "Screen flickering":
            facts['symptom'] = 'flickering'
        
        return facts