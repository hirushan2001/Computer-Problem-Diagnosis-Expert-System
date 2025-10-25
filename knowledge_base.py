"""
Computer Problem Diagnosis Expert System - Knowledge Base
Compatibility shim for Python 3.10+
"""

# Fix for Python 3.10+ compatibility with experta
import collections
import collections.abc as _collections_abc

for name in ("Mapping", "MutableMapping", "Sequence", "Iterable"):
    if not hasattr(collections, name):
        setattr(collections, name, getattr(_collections_abc, name))

from experta import *
import json


class ComputerDiagnosisSystem(KnowledgeEngine):
    """Expert System for Computer Problem Diagnosis"""
    
    def __init__(self):
        super().__init__()
        self.diagnosis_result = None
    
    @DefFacts()
    def initial_facts(self):
        """Initialize the system"""
        yield Fact(action="diagnose")
    
    # ==================== POWER & BOOT ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(power_status="not_turning_on"),
          Fact(power_cable="connected"),
          Fact(outlet_working="yes"),
          Fact(lights="none"))
    def diagnose_psu_failure(self):
        self.diagnosis_result = {
            'diagnosis': 'Power Supply Unit (PSU) Failure',
            'solution': '1. Check if PSU fan spins\n2. Test with PSU tester\n3. Replace PSU if confirmed dead\n4. Check power button connection to motherboard\n5. Verify PSU switch is ON',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(power_status="not_turning_on"),
          Fact(power_cable="connected"),
          Fact(outlet_working="yes"),
          Fact(lights="on"),
          Fact(display="no_signal"))
    def diagnose_display_or_ram(self):
        self.diagnosis_result = {
            'diagnosis': 'RAM, Graphics Card, or Display Issue',
            'solution': '1. Reseat RAM modules (remove and reinstall)\n2. Try one RAM stick at a time\n3. Reseat graphics card\n4. Check monitor cable connection\n5. Try different display cable/port\n6. Test with another monitor\n7. Listen for beep codes',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(power_status="turning_on"),
          Fact(boot_stage="no_bios"))
    def diagnose_motherboard_cpu(self):
        self.diagnosis_result = {
            'diagnosis': 'Motherboard or CPU Failure',
            'solution': '1. Reset CMOS (remove battery for 5 mins)\n2. Remove all unnecessary components\n3. Check for bent CPU pins\n4. Test with minimal hardware (CPU, 1 RAM, PSU)\n5. Check motherboard for burn marks\n6. Verify CPU cooler is properly mounted',
            'severity': 'critical'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(power_status="turning_on"),
          Fact(boot_stage="bios_shows"),
          Fact(boot_device="not_found"))
    def diagnose_boot_device(self):
        self.diagnosis_result = {
            'diagnosis': 'Boot Device Not Found',
            'solution': '1. Check boot order in BIOS\n2. Verify hard drive is detected in BIOS\n3. Check SATA/power cables to drive\n4. Try different SATA port\n5. Test drive in another system\n6. Boot from installation media to repair\n7. May need to rebuild BCD or reinstall OS',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(beep_code="1_long_2_short"))
    def diagnose_gpu_beep(self):
        self.diagnosis_result = {
            'diagnosis': 'Graphics Card Problem (Video Error)',
            'solution': '1. Reseat GPU firmly\n2. Check GPU power cables connected\n3. Try integrated graphics if available\n4. Test GPU in another system\n5. Clean GPU contacts with eraser\n6. Update BIOS\n7. Replace GPU if confirmed faulty',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(beep_code="continuous"))
    def diagnose_ram_beep(self):
        self.diagnosis_result = {
            'diagnosis': 'RAM Failure',
            'solution': '1. Remove all RAM sticks\n2. Install one stick at a time\n3. Try each slot individually\n4. Clean RAM contacts with eraser\n5. Test RAM with MemTest86\n6. Try known-good RAM\n7. Check motherboard RAM slots for damage',
            'severity': 'medium'
        }
    
    # ==================== PERFORMANCE ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="performance"),
          Fact(symptom="very_slow"),
          Fact(disk_type="hdd"),
          Fact(disk_health="poor"))
    def diagnose_failing_hdd(self):
        self.diagnosis_result = {
            'diagnosis': 'Failing Hard Drive',
            'solution': '1. BACKUP DATA IMMEDIATELY!\n2. Check SMART status with CrystalDiskInfo\n3. Run CHKDSK /F /R (may take hours)\n4. Replace drive urgently\n5. Consider cloning to SSD\n6. Check for clicking sounds (mechanical failure)',
            'severity': 'critical'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="performance"),
          Fact(symptom="very_slow"),
          Fact(cpu_usage="high"),
          Fact(process="unknown"))
    def diagnose_malware_performance(self):
        self.diagnosis_result = {
            'diagnosis': 'Possible Malware or Unwanted Software',
            'solution': '1. Check Task Manager for suspicious processes\n2. Run Windows Defender full scan\n3. Scan with Malwarebytes\n4. Boot to Safe Mode and scan\n5. Check startup programs (msconfig)\n6. Use Process Explorer to identify processes\n7. Remove suspicious programs\n8. Reset browsers if affected',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="performance"),
          Fact(symptom="very_slow"),
          Fact(ram_usage="high"),
          Fact(available_ram="low"))
    def diagnose_insufficient_ram(self):
        self.diagnosis_result = {
            'diagnosis': 'Insufficient RAM',
            'solution': '1. Close unnecessary programs\n2. Check Task Manager for memory hogs\n3. Disable startup programs\n4. Increase virtual memory (page file)\n5. Upgrade RAM (recommended)\n6. Check for memory leaks in applications\n7. Restart computer regularly',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="performance"),
          Fact(temperature="very_high"))
    def diagnose_overheating(self):
        self.diagnosis_result = {
            'diagnosis': 'System Overheating',
            'solution': '1. Clean dust from all fans and heatsinks\n2. Reapply thermal paste on CPU\n3. Check all fans are spinning\n4. Improve case airflow (cable management)\n5. Check CPU temperature with HWMonitor\n6. Verify CPU cooler is properly mounted\n7. Consider better cooling solution\n8. Check GPU temperature and cooling',
            'severity': 'high'
        }
    
    # ==================== BLUE SCREEN (BSOD) ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="bsod"),
          Fact(error_code="DRIVER_IRQL_NOT_LESS_OR_EQUAL"))
    def diagnose_driver_bsod(self):
        self.diagnosis_result = {
            'diagnosis': 'Driver Conflict (DRIVER_IRQL)',
            'solution': '1. Boot into Safe Mode\n2. Update all drivers (especially network/GPU)\n3. Rollback recently installed drivers\n4. Use Driver Verifier to find bad driver\n5. Check Windows Update\n6. Uninstall recent software\n7. Run SFC /scannow',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="bsod"),
          Fact(error_code="MEMORY_MANAGEMENT"))
    def diagnose_memory_bsod(self):
        self.diagnosis_result = {
            'diagnosis': 'Memory Management Error',
            'solution': '1. Run Windows Memory Diagnostic\n2. Test RAM with MemTest86 (8+ passes)\n3. Reseat all RAM modules\n4. Test one RAM stick at a time\n5. Update BIOS\n6. Reset BIOS to defaults\n7. Replace faulty RAM if confirmed\n8. Check for overclocking issues',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="bsod"),
          Fact(error_code="KERNEL_DATA_INPAGE_ERROR"))
    def diagnose_disk_bsod(self):
        self.diagnosis_result = {
            'diagnosis': 'Hard Drive or RAM Failure',
            'solution': '1. BACKUP DATA IMMEDIATELY!\n2. Run CHKDSK /F /R\n3. Check SMART status\n4. Test RAM with MemTest86\n5. Check SATA cables\n6. Try different SATA port\n7. Run disk manufacturer diagnostics\n8. Replace failing component',
            'severity': 'critical'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="bsod"),
          Fact(error_code="SYSTEM_SERVICE_EXCEPTION"))
    def diagnose_system_service_bsod(self):
        self.diagnosis_result = {
            'diagnosis': 'System Service or Driver Issue',
            'solution': '1. Update graphics drivers\n2. Run SFC /scannow\n3. Run DISM /Online /Cleanup-Image /RestoreHealth\n4. Check Windows Update\n5. Uninstall recent programs\n6. Boot to Safe Mode and troubleshoot\n7. Check Event Viewer for details',
            'severity': 'medium'
        }
    
    # ==================== BOOT PROBLEMS ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="boot"),
          Fact(symptom="boot_loop"),
          Fact(safe_mode="boots"))
    def diagnose_software_boot_loop(self):
        self.diagnosis_result = {
            'diagnosis': 'Software/Driver Causing Boot Loop',
            'solution': '1. Uninstall recent Windows updates\n2. Use System Restore to previous point\n3. Disable startup programs (msconfig)\n4. Run SFC and DISM repairs\n5. Uninstall recently installed software\n6. Update or rollback drivers\n7. Perform clean boot troubleshooting',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="boot"),
          Fact(symptom="boot_loop"),
          Fact(safe_mode="no_boot"))
    def diagnose_hardware_boot_loop(self):
        self.diagnosis_result = {
            'diagnosis': 'Hardware or Critical System Corruption',
            'solution': '1. Run Startup Repair from install media\n2. Rebuild BCD:\n   - bootrec /fixmbr\n   - bootrec /fixboot\n   - bootrec /rebuildbcd\n3. Test RAM thoroughly\n4. Check hard drive health\n5. Reset BIOS settings\n6. Consider clean Windows install\n7. Check hardware connections',
            'severity': 'critical'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="boot"),
          Fact(symptom="slow_boot"),
          Fact(boot_time=">5min"))
    def diagnose_slow_boot(self):
        self.diagnosis_result = {
            'diagnosis': 'Slow Boot Time',
            'solution': '1. Disable unnecessary startup programs\n2. Run Disk Cleanup\n3. Check for malware\n4. Update drivers\n5. Enable Fast Startup\n6. Defragment HDD (or optimize SSD)\n7. Consider upgrading to SSD\n8. Check disk health\n9. Disable unused services',
            'severity': 'medium'
        }
    
    # ==================== NETWORK ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="network"),
          Fact(symptom="no_internet"),
          Fact(other_devices="working"))
    def diagnose_pc_network_only(self):
        self.diagnosis_result = {
            'diagnosis': 'Network Adapter or Driver Issue',
            'solution': '1. Restart computer\n2. Update network adapter driver\n3. Uninstall and reinstall driver\n4. Run Network Troubleshooter\n5. Reset network settings:\n   - ipconfig /release\n   - ipconfig /renew\n   - ipconfig /flushdns\n   - netsh winsock reset\n   - netsh int ip reset\n6. Check if adapter is enabled\n7. Try Ethernet if using WiFi',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="network"),
          Fact(symptom="no_internet"),
          Fact(other_devices="not_working"))
    def diagnose_router_isp(self):
        self.diagnosis_result = {
            'diagnosis': 'Router or ISP Problem',
            'solution': '1. Power cycle modem and router (30 sec off)\n2. Check all cable connections\n3. Verify ISP service status online\n4. Check router admin panel for issues\n5. Try direct modem connection\n6. Reset router to factory settings (last resort)\n7. Contact ISP if problem persists',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="network"),
          Fact(symptom="slow_internet"),
          Fact(connection="wifi"),
          Fact(signal="weak"))
    def diagnose_wifi_signal(self):
        self.diagnosis_result = {
            'diagnosis': 'WiFi Signal/Interference Issue',
            'solution': '1. Move closer to router\n2. Remove physical obstructions\n3. Change WiFi channel (use WiFi analyzer app)\n4. Use 5GHz band if available\n5. Update router firmware\n6. Update WiFi adapter driver\n7. Consider WiFi extender or mesh system\n8. Avoid interference from microwaves/phones',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="network"),
          Fact(connection="wifi"),
          Fact(symptom="cannot_connect"),
          Fact(network_visible="yes"))
    def diagnose_wifi_auth(self):
        self.diagnosis_result = {
            'diagnosis': 'WiFi Authentication Issue',
            'solution': '1. Verify correct password\n2. Forget network and reconnect\n3. Restart router\n4. Check router security type (use WPA2)\n5. Disable MAC filtering temporarily\n6. Update router firmware\n7. Reset network settings on PC\n8. Try static IP assignment',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="network"),
          Fact(dns_working="no"),
          Fact(can_ping_ip="yes"))
    def diagnose_dns(self):
        self.diagnosis_result = {
            'diagnosis': 'DNS Resolution Problem',
            'solution': '1. Flush DNS cache: ipconfig /flushdns\n2. Change DNS to Google (8.8.8.8, 8.8.4.4) or Cloudflare (1.1.1.1)\n3. Restart DNS Client service\n4. Check hosts file (C:\\Windows\\System32\\drivers\\etc\\hosts)\n5. Reset TCP/IP: netsh int ip reset\n6. Disable IPv6 temporarily\n7. Clear browser cache',
            'severity': 'medium'
        }
    
    # ==================== APPLICATION ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="application"),
          Fact(symptom="crashes"),
          Fact(which_apps="specific"))
    def diagnose_specific_app_crash(self):
        self.diagnosis_result = {
            'diagnosis': 'Specific Application Problem',
            'solution': '1. Update the application to latest version\n2. Reinstall the application\n3. Run as administrator\n4. Check compatibility mode\n5. Check Event Viewer for crash details\n6. Disable antivirus temporarily\n7. Install missing dependencies (.NET, C++ Redistributables)\n8. Clear application cache/data\n9. Check if app needs GPU drivers update',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="application"),
          Fact(symptom="crashes"),
          Fact(which_apps="all"))
    def diagnose_system_app_crashes(self):
        self.diagnosis_result = {
            'diagnosis': 'System-wide Application Instability',
            'solution': '1. Run SFC /scannow\n2. Run DISM repair\n3. Update Windows\n4. Test RAM with MemTest86\n5. Update all drivers\n6. Update .NET Framework\n7. Scan for malware\n8. Check Event Viewer for patterns\n9. Perform clean boot\n10. May need Windows repair install',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="application"),
          Fact(symptom="wont_install"))
    def diagnose_install_failure(self):
        self.diagnosis_result = {
            'diagnosis': 'Software Installation Failure',
            'solution': '1. Run installer as administrator\n2. Disable antivirus temporarily\n3. Check system requirements\n4. Clean temp folders (Disk Cleanup)\n5. Ensure Windows Installer service is running\n6. Download installer again\n7. Check disk space\n8. Install in Safe Mode\n9. Check installer logs',
            'severity': 'low'
        }
    
    # ==================== PERIPHERAL ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="peripheral"),
          Fact(device="printer"),
          Fact(symptom="not_detected"))
    def diagnose_printer_not_found(self):
        self.diagnosis_result = {
            'diagnosis': 'Printer Not Detected',
            'solution': '1. Check USB/network cable connection\n2. Power cycle printer\n3. Restart Print Spooler service\n4. Update printer driver from manufacturer\n5. Remove and re-add printer\n6. Run printer troubleshooter\n7. Try different USB port\n8. Check if printer shows in Devices\n9. Disable firewall temporarily (network printer)',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="peripheral"),
          Fact(device="printer"),
          Fact(symptom="queue_stuck"))
    def diagnose_print_queue(self):
        self.diagnosis_result = {
            'diagnosis': 'Print Queue Stuck',
            'solution': '1. Cancel all print jobs\n2. Restart Print Spooler service:\n   - Open Services (services.msc)\n   - Stop Print Spooler\n   - Delete files from C:\\Windows\\System32\\spool\\PRINTERS\n   - Start Print Spooler\n3. Update printer driver\n4. Run printer troubleshooter\n5. Check printer connection',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="peripheral"),
          Fact(device="usb"),
          Fact(symptom="not_recognized"))
    def diagnose_usb_not_recognized(self):
        self.diagnosis_result = {
            'diagnosis': 'USB Device Not Recognized',
            'solution': '1. Try different USB port (USB 2.0 port recommended)\n2. Restart computer\n3. Update USB controller drivers\n4. Check Device Manager for errors (yellow exclamation)\n5. Test device on another computer\n6. Uninstall device in Device Manager, then reconnect\n7. Disable USB selective suspend\n8. Update chipset drivers\n9. Check if device needs external power',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="peripheral"),
          Fact(device="usb"),
          Fact(symptom="keeps_disconnecting"))
    def diagnose_usb_disconnecting(self):
        self.diagnosis_result = {
            'diagnosis': 'USB Device Keeps Disconnecting',
            'solution': '1. Try different USB port\n2. Disable USB selective suspend:\n   - Power Options > Change plan settings\n   - Change advanced power settings\n   - USB settings > Disable selective suspend\n3. Update USB drivers\n4. Check cable quality (replace if damaged)\n5. Try powered USB hub\n6. Update chipset drivers\n7. Check for loose connections',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="peripheral"),
          Fact(device="keyboard_mouse"),
          Fact(connection="wireless"),
          Fact(symptom="not_working"))
    def diagnose_wireless_kb_mouse(self):
        self.diagnosis_result = {
            'diagnosis': 'Wireless Keyboard/Mouse Issue',
            'solution': '1. Replace batteries\n2. Re-pair device (follow manufacturer steps)\n3. Plug USB receiver into different port\n4. Check for interference (move away from WiFi router)\n5. Update device driver\n6. Clean sensor/optical area\n7. Try on another computer\n8. Check if USB receiver is working (LED indicator)',
            'severity': 'low'
        }
    
    # ==================== AUDIO ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="audio"),
          Fact(symptom="no_sound"),
          Fact(device_detected="yes"),
          Fact(muted="no"))
    def diagnose_audio_output(self):
        self.diagnosis_result = {
            'diagnosis': 'Audio Output Configuration Issue',
            'solution': '1. Set correct default playback device:\n   - Right-click speaker icon\n   - Open Sound settings\n   - Choose correct output device\n2. Check app volume mixer (volume icon > mixer)\n3. Restart Windows Audio service\n4. Check speaker/headphone connection\n5. Test with different output device\n6. Disable audio enhancements\n7. Update audio driver\n8. Run audio troubleshooter',
            'severity': 'low'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="audio"),
          Fact(symptom="no_sound"),
          Fact(device_detected="no"))
    def diagnose_audio_driver(self):
        self.diagnosis_result = {
            'diagnosis': 'Audio Driver Problem',
            'solution': '1. Update audio driver from Device Manager\n2. Uninstall audio driver and restart (auto-reinstall)\n3. Download latest driver from manufacturer\n4. Check if audio device is disabled in Device Manager\n5. Enable audio device in BIOS\n6. Run audio troubleshooter\n7. Check for Windows updates\n8. Try generic High Definition Audio driver',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="audio"),
          Fact(symptom="crackling"))
    def diagnose_audio_quality(self):
        self.diagnosis_result = {
            'diagnosis': 'Audio Quality Issue (Crackling/Distortion)',
            'solution': '1. Update audio driver\n2. Change audio format:\n   - Sound settings > Properties\n   - Advanced tab\n   - Try 24-bit, 48000 Hz\n3. Disable audio enhancements\n4. Check CPU usage (may cause audio glitches)\n5. Update chipset drivers\n6. Check for electrical interference\n7. Try different speakers/headphones\n8. Adjust buffer size in audio settings',
            'severity': 'low'
        }
    
    # ==================== SECURITY ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="security"),
          Fact(symptom="malware_suspected"),
          OR(Fact(signs="popup_ads"),
             Fact(signs="slow_performance"),
             Fact(signs="unknown_programs"),
             Fact(signs="browser_redirects")))
    def diagnose_malware(self):
        self.diagnosis_result = {
            'diagnosis': 'Possible Malware Infection',
            'solution': '1. Disconnect from internet\n2. Boot into Safe Mode with Networking\n3. Run Windows Defender full scan\n4. Download and run Malwarebytes\n5. Run AdwCleaner\n6. Check Task Manager for suspicious processes\n7. Check startup programs (msconfig)\n8. Reset all browsers\n9. Change all passwords after cleanup\n10. Consider professional help if persistent',
            'severity': 'critical'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="security"),
          Fact(symptom="ransomware"))
    def diagnose_ransomware(self):
        self.diagnosis_result = {
            'diagnosis': 'Ransomware Attack',
            'solution': 'CRITICAL RESPONSE:\n1. IMMEDIATELY disconnect from network\n2. DO NOT pay ransom\n3. DO NOT delete encrypted files\n4. Take photo of ransom note\n5. Report to law enforcement\n6. Identify ransomware type (ID Ransomware website)\n7. Check if decryption tool exists\n8. Restore from backup if available\n9. Seek professional cybersecurity help\n10. Rebuild system from clean install',
            'severity': 'critical'
        }
    
    # ==================== STORAGE ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="storage"),
          Fact(symptom="disk_full"))
    def diagnose_disk_full(self):
        self.diagnosis_result = {
            'diagnosis': 'Disk Space Full',
            'solution': '1. Run Disk Cleanup (cleanmgr)\n2. Delete temp files: %temp% and C:\\Windows\\Temp\n3. Uninstall unused programs\n4. Use Storage Sense (Settings > Storage)\n5. Delete old Windows.old folder\n6. Empty Recycle Bin\n7. Move files to external drive\n8. Use WinDirStat to find large files\n9. Clear browser cache\n10. Consider adding storage',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="storage"),
          Fact(symptom="external_not_showing"))
    def diagnose_external_drive(self):
        self.diagnosis_result = {
            'diagnosis': 'External Drive Not Detected',
            'solution': '1. Try different USB port\n2. Check Disk Management (diskmgmt.msc)\n3. Assign drive letter manually if unallocated\n4. Update USB and storage drivers\n5. Test on another computer\n6. Check drive power supply (external power adapter)\n7. Try different USB cable\n8. Run CHKDSK if detected\n9. Initialize disk if brand new (Disk Management)',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="storage"),
          Fact(symptom="drive_errors"))
    def diagnose_drive_errors(self):
        self.diagnosis_result = {
            'diagnosis': 'Hard Drive Errors',
            'solution': 'URGENT:\n1. BACKUP DATA IMMEDIATELY!\n2. Run CHKDSK /F /R (takes hours, be patient)\n3. Check SMART status with CrystalDiskInfo\n4. Run manufacturer diagnostics tool\n5. Listen for clicking/grinding sounds\n6. Check disk health percentage\n7. If critical, clone to new drive ASAP\n8. Replace drive if showing failures\n9. Monitor temperature',
            'severity': 'critical'
        }
    
    # ==================== WINDOWS UPDATE ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="windows_update"),
          Fact(symptom="update_failing"))
    def diagnose_update_fail(self):
        self.diagnosis_result = {
            'diagnosis': 'Windows Update Failure',
            'solution': '1. Run Windows Update Troubleshooter\n2. Clear Windows Update cache:\n   - Stop Windows Update service\n   - Delete C:\\Windows\\SoftwareDistribution\n   - Start Windows Update service\n3. Run: DISM /Online /Cleanup-Image /RestoreHealth\n4. Run: SFC /scannow\n5. Check disk space (need 20GB+)\n6. Manually download update from catalog\n7. Disable antivirus temporarily\n8. Try offline update',
            'severity': 'medium'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="windows_update"),
          Fact(symptom="update_stuck"))
    def diagnose_update_stuck(self):
        self.diagnosis_result = {
            'diagnosis': 'Windows Update Stuck',
            'solution': '1. Wait at least 2-3 hours (can take very long)\n2. Check if HDD light is blinking (still working)\n3. If truly frozen (4+ hours, no disk activity):\n   - Force restart (hold power button)\n4. Boot into Safe Mode\n5. Run Update Troubleshooter\n6. Clear update cache\n7. Try again or use Media Creation Tool\n8. For major updates, use Update Assistant',
            'severity': 'medium'
        }
    
    # ==================== DISPLAY ISSUES ====================
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="display"),
          Fact(symptom="no_display"),
          Fact(power_on="yes"))
    def diagnose_no_display_power_on(self):
        self.diagnosis_result = {
            'diagnosis': 'No Display with Power On',
            'solution': '1. Check monitor power and connections\n2. Try different video cable\n3. Try different video port (HDMI/DisplayPort/VGA)\n4. Test with another monitor\n5. Reseat graphics card\n6. Try integrated graphics if available\n7. Check if monitor input source is correct\n8. Listen for beep codes',
            'severity': 'high'
        }
    
    @Rule(Fact(action='diagnose'),
          Fact(issue_category="display"),
          Fact(symptom="flickering"))
    def diagnose_screen_flickering(self):
        self.diagnosis_result = {
            'diagnosis': 'Screen Flickering',
            'solution': '1. Update graphics driver\n2. Check refresh rate setting (60Hz recommended)\n3. Try different cable\n4. Disable hardware acceleration in apps\n5. Check for loose connections\n6. Update monitor firmware\n7. Test with different monitor\n8. Check GPU temperature\n9. Reseat GPU',
            'severity': 'low'
        }
    
    # ==================== DEFAULT CATCH-ALL ====================
    
    @Rule(Fact(action='diagnose'))
    def general_troubleshooting(self):
        """Catch-all rule with lowest priority"""
        if not self.diagnosis_result:
            self.diagnosis_result = {
                'diagnosis': 'General Computer Issue - Basic Troubleshooting',
                'solution': '1. Restart computer\n2. Check all physical connections\n3. Run Windows Update\n4. Update all drivers\n5. Run antivirus scan\n6. Check Event Viewer for errors\n7. Run SFC /scannow\n8. Check Task Manager for resource usage\n9. Clean temp files\n10. Check for overheating',
                'severity': 'low'
            }


def save_diagnosis(diagnosis_data):
    """Save diagnosis history to JSON file"""
    try:
        try:
            with open('diagnosis_history.json', 'r') as f:
                history = json.load(f)
        except FileNotFoundError:
            history = []
        
        history.append(diagnosis_data)
        
        with open('diagnosis_history.json', 'w') as f:
            json.dump(history, f, indent=2)
        return True
    except Exception as e:
        print(f"Warning: Could not save diagnosis history: {e}")
        return False