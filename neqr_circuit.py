from qiskit import QuantumCircuit

from config import TOTAL_QUBITS, POSITION_QUBITS
from image_data import image
import secret_data


def create_circuit():

    qc = QuantumCircuit(TOTAL_QUBITS, TOTAL_QUBITS)

    """
    q0 -> v1
    q1 -> v0
    q2 -> p1
    q3 -> p0
    """

    # =====================================================
    # STEP 1 : POSITION SUPERPOSITION
    # =====================================================

    for qubit in range(
        TOTAL_QUBITS - POSITION_QUBITS,
        TOTAL_QUBITS
    ):
        qc.h(qubit)

    # =====================================================
    # STEP 2 : STEGO-STATE ENCODING
    # =====================================================

    for row in range(2):

        for col in range(2):

            # pixel value
            pixel_value = image[row][col]

            binary_value = format(
                pixel_value,
                '02b'
            )

            # =============================================
            # SECRET + KEY
            # =============================================

            secret_index = row * 2 + col

            secret_bit = int(
                secret_data.secret_message[
                    secret_index
                ]
            )

            key_bit = int(
                secret_data.secret_key[
                    secret_index
                ]
            )

            # =============================================
            # ORIGINAL IMAGE BIT
            # =============================================

            original_v1 = binary_value[0]

            # blind key-based encoding
            stego_v0 = secret_bit ^ key_bit

            final_v1 = original_v1
            final_v0 = str(stego_v0)

            # =============================================
            # POSITION BITS
            # =============================================

            p1 = format(row, '01b')
            p0 = format(col, '01b')

            # =============================================
            # PREPARE CONTROLS
            # =============================================

            if p1 == '0':
                qc.x(2)

            if p0 == '0':
                qc.x(3)

            # =============================================
            # ENCODE v1
            # =============================================

            if final_v1 == '1':
                qc.ccx(2, 3, 0)

            # =============================================
            # ENCODE v0
            # =============================================

            if final_v0 == '1':
                qc.ccx(2, 3, 1)

            # =============================================
            # RESTORE POSITION QUBITS
            # =============================================

            if p1 == '0':
                qc.x(2)

            if p0 == '0':
                qc.x(3)

    return qc
