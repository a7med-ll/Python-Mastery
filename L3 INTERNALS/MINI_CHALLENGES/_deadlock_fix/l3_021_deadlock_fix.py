import threading
import time


# -----------------------------------------------------------------------------
# Deadlock Example
# -----------------------------------------------------------------------------

class l3_021DeadlockExample:

    def __init__(self) -> None:

        # Create first lock resource.
        self._lock_a = threading.Lock()

        # Create second lock resource.
        self._lock_b = threading.Lock()


    # -------------------------------------------------------------------------
    # Thread One
    # -------------------------------------------------------------------------

    def l3_021ThreadOne(self) -> None:

        print("Thread One acquiring lock A")

        # Acquire lock A first.
        self._lock_a.acquire()

        print("Thread One acquired lock A")

        # Give thread two time to acquire lock B.
        time.sleep(1)

        print("Thread One waiting for lock B")

        # Wait for lock B.
        self._lock_b.acquire()

        print("Thread One acquired lock B")


    # -------------------------------------------------------------------------
    # Thread Two
    # -------------------------------------------------------------------------

    def l3_021ThreadTwo(self) -> None:

        print("Thread Two acquiring lock B")

        # Acquire lock B first.
        self._lock_b.acquire()

        print("Thread Two acquired lock B")

        # Give thread one time to acquire lock A.
        time.sleep(1)

        print("Thread Two waiting for lock A")

        # Wait for lock A.
        self._lock_a.acquire()

        print("Thread Two acquired lock A")


# -----------------------------------------------------------------------------
# Fixed Deadlock Version
# -----------------------------------------------------------------------------

class l3_021DeadlockFixed:

    def __init__(self) -> None:

        # Create first lock resource.
        self._lock_a = threading.Lock()

        # Create second lock resource.
        self._lock_b = threading.Lock()


    # -------------------------------------------------------------------------
    # Thread One
    # -------------------------------------------------------------------------

    def l3_021FixedThreadOne(self) -> None:

        print("Fixed Thread One acquiring lock A")

        # Acquire locks in fixed order.
        with self._lock_a:

            print("Fixed Thread One acquired lock A")

            time.sleep(1)

            with self._lock_b:

                print("Fixed Thread One acquired lock B")


    # -------------------------------------------------------------------------
    # Thread Two
    # -------------------------------------------------------------------------

    def l3_021FixedThreadTwo(self) -> None:

        print("Fixed Thread Two acquiring lock A")

        # Acquire locks in same order.
        with self._lock_a:

            print("Fixed Thread Two acquired lock A")

            time.sleep(1)

            with self._lock_b:

                print("Fixed Thread Two acquired lock B")


# -----------------------------------------------------------------------------
# Runner
# -----------------------------------------------------------------------------

def run_l3_021DeadlockExample() -> None:

    print("=" * 70)
    print("L3-021 Deadlock Example")
    print("=" * 70)


    # -------------------------------------------------------------------------
    # Test 1: Deadlock Detection
    # -------------------------------------------------------------------------

    print("\n[TEST 1] Deadlock Detection")
    print("-" * 70)

    # Create deadlock object.
    deadlock_example = l3_021DeadlockExample()

    # Create threads.
    thread_1 = threading.Thread(
        target=deadlock_example.l3_021ThreadOne
    )

    thread_2 = threading.Thread(
        target=deadlock_example.l3_021ThreadTwo
    )

    # Start threads.
    thread_1.start()
    thread_2.start()

    # Wait with timeout.
    thread_1.join(timeout=3)
    thread_2.join(timeout=3)

    # Check deadlock.
    if thread_1.is_alive() or thread_2.is_alive():

        print("\nDeadlock detected")

    else:

        print("\nNo deadlock detected")


    # -------------------------------------------------------------------------
    # Test 2: Fixed Version
    # -------------------------------------------------------------------------

    print("\n[TEST 2] Fixed Deadlock")
    print("-" * 70)

    # Create fixed object.
    fixed_example = l3_021DeadlockFixed()

    # Create fixed threads.
    fixed_thread_1 = threading.Thread(
        target=fixed_example.l3_021FixedThreadOne
    )

    fixed_thread_2 = threading.Thread(
        target=fixed_example.l3_021FixedThreadTwo
    )

    # Start fixed threads.
    fixed_thread_1.start()
    fixed_thread_2.start()

    # Wait for completion.
    fixed_thread_1.join()
    fixed_thread_2.join()

    print("\nNo deadlock detected")


    print("=" * 70)
    print("L3-021 Completed Successfully")
    print("=" * 70)


if __name__ == "__main__":
    run_l3_021DeadlockExample()