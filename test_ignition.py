from core.config_loader import AxonConfig
from core.bridge import AxonBridge


def run_diagnostics():
    print("="*40)
    print("INITIATING AXON DIAGNOSTICS")
    print("="*40)

    # Test 1: Identity
    try:
        config = AxonConfig()
        print(f"Config Loader : ONLINE")
        print(f"   Identity    : {config.context_header}")
    except Exception as e:
        print(f"Config Error: {e}")
        return

    # Test 2: Google Handshake
    print("\n Attempting Google Drive Handshake...")
    print("   (Check your browser if this is the first run!)")
    try:
        bridge = AxonBridge()
        print(f"Cloud Bridge  : ONLINE")
        print("   Token Status  : Secured.")
    except Exception as e:
        print(f"Bridge Error  : {e}")

    print("="*40)


if __name__ == "__main__":
    run_diagnostics()
