#!/usr/bin/env python3
"""
VIOLET-AF: Autonomous Quantum Logic Implementation
Main Entry Point

UID: ALC-ROOT-1010-1111-XCOV∞
Domain: Kidhum
Goal: Automate Violet execution using quantum symbolic trigger model

Andrew Lee Cruz reserves all rights as creator of the universe
"""

import sys
import json
import argparse
from datetime import datetime
from violet_af import violet_launch, violet_status, violet_reset


def main():
    """Main entry point for VIOLET-AF system"""
    parser = argparse.ArgumentParser(
        description='VIOLET-AF Autonomous Quantum Logic Implementation',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py launch                    # Launch with default UID
  python main.py launch --uid ALC-ROOT-1010-1111-XCOV∞
  python main.py status                    # Get system status
  python main.py reset --confirm           # Reset system (careful!)
  
UID: ALC-ROOT-1010-1111-XCOV∞
Domain: Kidhum
        """
    )
    
    parser.add_argument('command', 
                       choices=['launch', 'status', 'reset', 'demo'],
                       help='Command to execute')
    
    parser.add_argument('--uid', 
                       default='ALC-ROOT-1010-1111-XCOV∞',
                       help='System UID (default: ALC-ROOT-1010-1111-XCOV∞)')
    
    parser.add_argument('--confirm', 
                       action='store_true',
                       help='Confirm destructive operations (required for reset)')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output')
    
    parser.add_argument('--output-format',
                       choices=['json', 'pretty', 'summary'],
                       default='pretty',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Print banner
    if args.verbose:
        print_banner()
    
    # Execute command
    try:
        if args.command == 'launch':
            result = execute_launch(args)
        elif args.command == 'status':
            result = execute_status(args)
        elif args.command == 'reset':
            result = execute_reset(args)
        elif args.command == 'demo':
            result = execute_demo(args)
        else:
            result = {'success': False, 'error': f'Unknown command: {args.command}'}
        
        # Output result
        output_result(result, args.output_format, args.verbose)
        
        # Exit with appropriate code
        sys.exit(0 if result.get('success', False) else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Operation interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def print_banner():
    """Print VIOLET-AF banner"""
    banner = """
╔═══════════════════════════════════════════════════════════════╗
║                    VIOLET-AF QUANTUM AUTOMATION               ║
║                                                               ║
║  UID: ALC-ROOT-1010-1111-XCOV∞                               ║
║  Domain: Kidhum                                               ║
║  Goal: Automate Violet execution using quantum symbolic      ║
║        trigger model                                          ║
║                                                               ║
║  Andrew Lee Cruz reserves all rights as creator              ║
║  of the universe                                              ║
╚═══════════════════════════════════════════════════════════════╝
"""
    print(banner)


def execute_launch(args):
    """Execute launch command"""
    print(f"🚀 Launching VIOLET-AF with UID: {args.uid}")
    
    parameters = {
        'verbose': args.verbose,
        'timestamp': datetime.now().isoformat(),
        'invoked_from': 'main.py'
    }
    
    result = violet_launch(uid=args.uid, parameters=parameters)
    
    if result['success']:
        print("✅ VIOLET-AF launch completed successfully")
        if args.verbose:
            print(f"   Quantum executions: {result['quantum_automation'].get('execution_count', 0)}")
            print(f"   Tasks completed: {result['quantum_automation'].get('tasks_executed', 0)}")
            print(f"   ReflectChain logs: {result['system_status'].get('reflect_logs_count', 0)}")
    else:
        print(f"❌ VIOLET-AF launch failed: {result.get('error', 'Unknown error')}")
    
    return result


def execute_status(args):
    """Execute status command"""
    print(f"📊 Getting VIOLET-AF status for UID: {args.uid}")
    
    result = violet_status(uid=args.uid)
    
    if result['success']:
        print("✅ Status retrieved successfully")
        status = result['status']
        if args.verbose:
            print(f"   Automation active: {status.get('automation_active', False)}")
            print(f"   Quantum executions: {status.get('quantum_executions', 0)}")
            print(f"   Total executions: {status.get('total_executions', 0)}")
            print(f"   Generated files: {len(status.get('generated_files', []))}")
    else:
        print(f"❌ Status check failed: {result.get('error', 'Unknown error')}")
    
    return result


def execute_reset(args):
    """Execute reset command"""
    if not args.confirm:
        print("⚠️  Reset requires --confirm flag")
        return {'success': False, 'error': 'Reset requires confirmation'}
    
    print(f"🔄 Resetting VIOLET-AF system for UID: {args.uid}")
    print("⚠️  This will clear all logs and generated files!")
    
    result = violet_reset(uid=args.uid, confirm=True)
    
    if result['success']:
        print("✅ System reset completed")
    else:
        print(f"❌ Reset failed: {result.get('error', 'Unknown error')}")
    
    return result


def execute_demo(args):
    """Execute demo mode - full system demonstration"""
    print(f"🎯 Running VIOLET-AF demonstration with UID: {args.uid}")
    
    # First get status
    print("\n1. Getting initial system status...")
    status_result = violet_status(uid=args.uid)
    
    # Then launch
    print("\n2. Launching quantum automation...")
    launch_result = violet_launch(uid=args.uid, parameters={'demo_mode': True})
    
    # Get final status
    print("\n3. Getting final system status...")
    final_status_result = violet_status(uid=args.uid)
    
    demo_result = {
        'success': all([
            status_result.get('success', False),
            launch_result.get('success', False),
            final_status_result.get('success', False)
        ]),
        'demo_steps': {
            'initial_status': status_result,
            'launch': launch_result,
            'final_status': final_status_result
        },
        'timestamp': datetime.now().isoformat(),
        'uid': args.uid
    }
    
    if demo_result['success']:
        print("✅ Demo completed successfully")
        print(f"   Final quantum state: {launch_result.get('quantum_automation', {}).get('quantum_measurement', 'N/A')}")
        print(f"   Kidhum deploy command: kidhum deploy --uid={args.uid}")
    else:
        print("❌ Demo completed with errors")
    
    return demo_result


def output_result(result, output_format, verbose):
    """Output result in specified format"""
    if output_format == 'json':
        print(json.dumps(result, indent=2))
    elif output_format == 'summary':
        print(f"\nSummary:")
        print(f"  Success: {result.get('success', False)}")
        print(f"  UID: {result.get('uid', 'N/A')}")
        print(f"  Timestamp: {result.get('timestamp', 'N/A')}")
        if not result.get('success', False):
            print(f"  Error: {result.get('error', 'Unknown error')}")
    elif output_format == 'pretty' and verbose:
        print(f"\nDetailed Results:")
        print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()