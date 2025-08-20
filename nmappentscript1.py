#!/usr/bin/env python3
"""
Automatización de Pentesting con Nmap
Herramienta para automatizar las fases de reconocimiento y enumeración
"""

import subprocess
import json
import xml.etree.ElementTree as ET
import argparse
import sys
import os
from datetime import datetime
import threading
import time

class NmapPentester:
    def __init__(self, target, output_dir="pentest_results"):
        self.target = target
        self.output_dir = output_dir
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.results = {}
        
        # Crear directorio de resultados
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def log(self, message):
        """Función para logging con timestamp"""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
    
    def run_nmap_command(self, command, description, output_file):
        """Ejecutar comandos nmap y guardar resultados"""
        self.log(f"Ejecutando: {description}")
        full_command = command + ["-oX", f"{self.output_dir}/{output_file}"]
        
        try:
            result = subprocess.run(full_command, capture_output=True, text=True, timeout=300)
            if result.returncode == 0:
                self.log(f"✓ Completado: {description}")
                return True
            else:
                self.log(f"✗ Error en {description}: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            self.log(f"✗ Timeout en {description}")
            return False
        except Exception as e:
            self.log(f"✗ Excepción en {description}: {str(e)}")
            return False
    
    def host_discovery(self):
        """Fase 1: Descubrimiento de hosts"""
        self.log("=== FASE 1: DESCUBRIMIENTO DE HOSTS ===")
        
        # Ping scan
        ping_cmd = ["nmap", "-sn", "-PE", "-PP", "-PM", self.target]
        self.run_nmap_command(ping_cmd, "Ping Scan", f"ping_scan_{self.timestamp}.xml")
        
        # ARP scan (si es red local)
        if "/" in self.target:
            arp_cmd = ["nmap", "-sn", "-PR", self.target]
            self.run_nmap_command(arp_cmd, "ARP Scan", f"arp_scan_{self.timestamp}.xml")
    
    def port_scanning(self):
        """Fase 2: Escaneo de puertos"""
        self.log("=== FASE 2: ESCANEO DE PUERTOS ===")
        
        # TCP SYN Scan - puertos comunes
        syn_cmd = ["nmap", "-sS", "-F", self.target]
        self.run_nmap_command(syn_cmd, "TCP SYN Scan (puertos comunes)", f"tcp_syn_fast_{self.timestamp}.xml")
        
        # TCP Connect Scan - top 1000 puertos
        connect_cmd = ["nmap", "-sT", "--top-ports", "1000", self.target]
        self.run_nmap_command(connect_cmd, "TCP Connect Scan (top 1000)", f"tcp_connect_{self.timestamp}.xml")
        
        # UDP Scan - puertos comunes
        udp_cmd = ["nmap", "-sU", "--top-ports", "100", self.target]
        self.run_nmap_command(udp_cmd, "UDP Scan (top 100)", f"udp_scan_{self.timestamp}.xml")
    
    def service_detection(self):
        """Fase 3: Detección de servicios y versiones"""
        self.log("=== FASE 3: DETECCIÓN DE SERVICIOS ===")
        
        # Service detection
        service_cmd = ["nmap", "-sV", "-sC", "--top-ports", "1000", self.target]
        self.run_nmap_command(service_cmd, "Detección de servicios y scripts", f"service_detection_{self.timestamp}.xml")
        
        # OS detection
        os_cmd = ["nmap", "-O", self.target]
        self.run_nmap_command(os_cmd, "Detección de OS", f"os_detection_{self.timestamp}.xml")
    
    def vulnerability_scanning(self):
        """Fase 4: Escaneo de vulnerabilidades"""
        self.log("=== FASE 4: ESCANEO DE VULNERABILIDADES ===")
        
        # Vulnerability scripts
        vuln_cmd = ["nmap", "--script", "vuln", self.target]
        self.run_nmap_command(vuln_cmd, "Scripts de vulnerabilidades", f"vuln_scan_{self.timestamp}.xml")
        
        # SMB vulnerabilities
        smb_cmd = ["nmap", "--script", "smb-vuln*", "-p", "139,445", self.target]
        self.run_nmap_command(smb_cmd, "Vulnerabilidades SMB", f"smb_vuln_{self.timestamp}.xml")
        
        # HTTP vulnerabilities
        http_cmd = ["nmap", "--script", "http-vuln*", "-p", "80,443,8080,8443", self.target]
        self.run_nmap_command(http_cmd, "Vulnerabilidades HTTP", f"http_vuln_{self.timestamp}.xml")
    
    def aggressive_scan(self):
        """Fase 5: Escaneo agresivo"""
        self.log("=== FASE 5: ESCANEO AGRESIVO ===")
        
        # Aggressive scan
        aggressive_cmd = ["nmap", "-A", "-T4", self.target]
        self.run_nmap_command(aggressive_cmd, "Escaneo agresivo", f"aggressive_{self.timestamp}.xml")
    
    def stealth_scan(self):
        """Escaneo sigiloso"""
        self.log("=== ESCANEO SIGILOSO ===")
        
        # Stealth scan
        stealth_cmd = ["nmap", "-sS", "-T2", "-f", self.target]
        self.run_nmap_command(stealth_cmd, "Escaneo sigiloso", f"stealth_{self.timestamp}.xml")
    
    def parse_xml_results(self):
        """Parsear resultados XML y generar resumen"""
        self.log("=== GENERANDO RESUMEN DE RESULTADOS ===")
        
        summary = {
            "target": self.target,
            "timestamp": self.timestamp,
            "hosts": [],
            "open_ports": [],
            "vulnerabilities": []
        }
        
        # Buscar todos los archivos XML generados
        xml_files = [f for f in os.listdir(self.output_dir) if f.endswith('.xml') and self.timestamp in f]
        
        for xml_file in xml_files:
            try:
                tree = ET.parse(f"{self.output_dir}/{xml_file}")
                root = tree.getroot()
                
                # Extraer hosts
                for host in root.findall('.//host'):
                    status = host.find('status')
                    if status is not None and status.get('state') == 'up':
                        address = host.find('address')
                        if address is not None:
                            ip = address.get('addr')
                            if ip not in [h['ip'] for h in summary['hosts']]:
                                summary['hosts'].append({'ip': ip})
                
                # Extraer puertos abiertos
                for port in root.findall('.//port'):
                    state = port.find('state')
                    if state is not None and state.get('state') == 'open':
                        portid = port.get('portid')
                        protocol = port.get('protocol')
                        service = port.find('service')
                        service_name = service.get('name') if service is not None else 'unknown'
                        
                        port_info = f"{portid}/{protocol} ({service_name})"
                        if port_info not in summary['open_ports']:
                            summary['open_ports'].append(port_info)
                
                # Extraer vulnerabilidades (de scripts)
                for script in root.findall('.//script'):
                    script_id = script.get('id')
                    if 'vuln' in script_id.lower():
                        output = script.get('output', '')
                        if 'VULNERABLE' in output.upper():
                            summary['vulnerabilities'].append({
                                'script': script_id,
                                'output': output[:200] + '...' if len(output) > 200 else output
                            })
            
            except Exception as e:
                self.log(f"Error parseando {xml_file}: {str(e)}")
        
        # Guardar resumen
        with open(f"{self.output_dir}/summary_{self.timestamp}.json", 'w') as f:
            json.dump(summary, f, indent=2)
        
        self.generate_report(summary)
    
    def generate_report(self, summary):
        """Generar reporte final"""
        report_file = f"{self.output_dir}/report_{self.timestamp}.txt"
        
        with open(report_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("REPORTE DE PENTESTING AUTOMATIZADO\n")
            f.write("=" * 60 + "\n")
            f.write(f"Target: {summary['target']}\n")
            f.write(f"Timestamp: {summary['timestamp']}\n")
            f.write("=" * 60 + "\n\n")
            
            f.write("HOSTS ENCONTRADOS:\n")
            f.write("-" * 20 + "\n")
            for host in summary['hosts']:
                f.write(f"• {host['ip']}\n")
            f.write(f"\nTotal: {len(summary['hosts'])} hosts\n\n")
            
            f.write("PUERTOS ABIERTOS:\n")
            f.write("-" * 20 + "\n")
            for port in summary['open_ports']:
                f.write(f"• {port}\n")
            f.write(f"\nTotal: {len(summary['open_ports'])} puertos\n\n")
            
            f.write("VULNERABILIDADES DETECTADAS:\n")
            f.write("-" * 30 + "\n")
            if summary['vulnerabilities']:
                for vuln in summary['vulnerabilities']:
                    f.write(f"• {vuln['script']}\n")
                    f.write(f"  {vuln['output']}\n\n")
            else:
                f.write("No se detectaron vulnerabilidades obvias.\n")
            
            f.write("=" * 60 + "\n")
            f.write("ARCHIVOS GENERADOS:\n")
            f.write(f"• Directorio: {self.output_dir}/\n")
            f.write(f"• Resumen JSON: summary_{self.timestamp}.json\n")
            f.write(f"• Reporte: report_{self.timestamp}.txt\n")
            f.write("• Archivos XML de nmap: *_{}.xml\n".format(self.timestamp))
        
        self.log(f"✓ Reporte generado: {report_file}")
    
    def run_full_scan(self, include_stealth=False):
        """Ejecutar escaneo completo"""
        start_time = time.time()
        self.log(f"Iniciando pentesting automatizado para: {self.target}")
        
        try:
            self.host_discovery()
            self.port_scanning()
            self.service_detection()
            self.vulnerability_scanning()
            self.aggressive_scan()
            
            if include_stealth:
                self.stealth_scan()
            
            self.parse_xml_results()
            
            elapsed_time = time.time() - start_time
            self.log(f"✓ Pentesting completado en {elapsed_time:.2f} segundos")
            
        except KeyboardInterrupt:
            self.log("✗ Pentesting interrumpido por el usuario")
        except Exception as e:
            self.log(f"✗ Error durante el pentesting: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description="Automatización de Pentesting con Nmap")
    parser.add_argument("target", help="Target IP/CIDR/hostname")
    parser.add_argument("-o", "--output", default="pentest_results", 
                       help="Directorio de salida (default: pentest_results)")
    parser.add_argument("-s", "--stealth", action="store_true", 
                       help="Incluir escaneo sigiloso")
    parser.add_argument("--quick", action="store_true", 
                       help="Escaneo rápido (solo puertos y servicios)")
    
    args = parser.parse_args()
    
    # Verificar si nmap está instalado
    try:
        subprocess.run(["nmap", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: nmap no está instalado o no está en el PATH")
        sys.exit(1)
    
    pentester = NmapPentester(args.target, args.output)
    
    if args.quick:
        pentester.log("=== MODO RÁPIDO ===")
        pentester.port_scanning()
        pentester.service_detection()
        pentester.parse_xml_results()
    else:
        pentester.run_full_scan(args.stealth)

if __name__ == "__main__":
    main()
