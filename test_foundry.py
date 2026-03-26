import os


from core.config_loader import AxonConfig
from core.foundry import AxonFoundry


def run_forge_test():
    print("="*40)
    print("INITIATING AXON FOUNDRY")
    print("="*40)

    # 1. Load your identity
    config = AxonConfig()
    foundry = AxonFoundry()

    # 2. Prepare the context (merging your static ID with dynamic project info)
    document_context = {
        "full_name": config.full_name,
        "student_id": config.student_id,
        "primary_role": config.primary_role,
        "project_title": "Project Axon Initialization",
        "objective": "To create a comprehensive documentation system for the Axon project."
    }

    # 3. Forge the document
    template_name = "Axon_Test_File.docx"
    output_name = "Axon_Test_Output.docx"

    try:
        print(f"Forging {output_name}...")
        result_path = foundry.generate_docx(
            template_name, document_context, output_name)
        print(f"Success! File saved to: {result_path}")
    except Exception as e:
        print(f"Forge Failed: {e}")


if __name__ == "__main__":
    run_forge_test()
